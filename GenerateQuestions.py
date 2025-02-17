import Asking, Parser
import spacy

class GenerateQuestions(object):

	def __init__(self):
		textfile = "test.txt"
		self.nlp = spacy.load('en_core_web_sm')
		self.asker = Asking.Asking(textfile)
		self.parser = Parser.Parser(textfile)

	# Refine questions by deleting words of a sentence surrounded by commas or
	# making them into their own sentence
	def splitCommas(self, sentence, root, ner_tags):
		if "," not in sentence:
			return sentence
		deleteParts = set()
		splitSentence = sentence.split(",")[1:]

		# if root is not in part surrounded by commas and part is not long,
		# delete part
		# edge case: if there are words like because, since, which, due to
		for part in splitSentence:
			partLen = len(part.split())
			if partLen < 5 and root not in part:
				if ('because' not in part) and ('since' not in part) and \
						('which' not in part) and ('due to' not in part):
					for tag in ner_tags:
						if tag not in part:
							deleteParts.add(part)
		# delete unnecessary parts from original sentence
		for part in deleteParts:
			sentence = sentence.replace(part, "")
		return sentence

	def checkSentenceType(self, sentence, dep_dict, ner_tag_dict, root):
		possible_types = set()
		if ("TIME" in ner_tag_dict.values()) or (
				"DATE" in ner_tag_dict.values()):
			possible_types.add("When")
		if ("PERSON" in ner_tag_dict.values()):
			possible_types.add("Who")
		if ("FAC" in ner_tag_dict.values()) or (
				"ORG" in ner_tag_dict.values()) or (
				"LOC" in ner_tag_dict.values()) or (
				"GPE" in ner_tag_dict.values()):
			possible_types.add("Where")
		if ("MONEY" in ner_tag_dict.values()):
			possible_types.add("How much")
		if ("DATE" in ner_tag_dict.values()):
			possible_types.add("How long")
		if ("CARDINAL" in ner_tag_dict.values()):
			possible_types.add("How many")
			possible_types.add("How often")
		if ("because" in sentence) or ("due to" in sentence) or (
				"Due to" in sentence) or ("since" in sentence):
			possible_types.add("Why")
		aux_verbs = {"are", "is", "was", "were", "shall", "do", "does", "did",
					 "can", "could", "have", "need", "should", "will", "would",
					 "must", "may", "might", "cannot"}
		if root in aux_verbs:
			possible_types.add("What")
		for dep in dep_dict.values():
			if dep[0] == 'nsubj':
				possible_types.add("What")
		return possible_types

	def generateQuestions(self, limit):
		possible_questions = set()
		for sentence in self.parser.text:
			print("SENTENCE: ", sentence)

			nlp_doc = self.nlp(sentence)
			token_dict, root = self.parser.dependency_dict(nlp_doc)
			ner_tags = self.parser.ner_tag_sentence(sentence)
			# redo NER tagging, POS tagging, etc after unnecessary commas removed
			# sentence = self.splitCommas(sentence, root, ner_tags)
			# print("NEW SENTENCE: ", sentence)
			nlp_doc = self.nlp(sentence)
			pos_tags = self.parser.pos_tag_sentence(sentence)
			token_dict, root = self.parser.dependency_dict(nlp_doc)
			ner_tags = self.parser.ner_tag_sentence(sentence)
			lemma_dict = self.parser.getTokenLemma(nlp_doc)

			type_dict = {"How many": self.asker.howManyQ(sentence, ner_tags,
												token_dict, pos_tags, root),
						 "Who": self.asker.whoQ(sentence, ner_tags, token_dict),
						 "How much": self.asker.howMuchQ(sentence, nlp_doc, ner_tags,
													  token_dict, root, pos_tags),
						 "How often": self.asker.howOftenQ(sentence, ner_tags, token_dict,
														pos_tags, root),
						 "Why": self.asker.whyQ(sentence, nlp_doc, ner_tags, token_dict,
											 pos_tags, root),
						 "Where": self.asker.whereQ(sentence, token_dict, pos_tags),
						 "What": self.asker.whatQ(sentence, token_dict, root, pos_tags,
											   lemma_dict),
						 "When": self.asker.whenQ(sentence, ner_tags, root, nlp_doc,
											   pos_tags)}

			# generate question outputs
			possible_types = self.checkSentenceType(sentence, token_dict,
													ner_tags, root)
			for type in possible_types:
				try:
					question = type_dict[type]
					if self.isValidQuestion(question):
						print("VALID Q: ", question)
						possible_questions.add(question)
				except:
					print("ERROR HERE")
					continue

				# check if binary question is possible
			binary_output = self.asker.binaryQ(sentence, root)
			if self.isValidQuestion(binary_output):
				print("BINARY Q: ", binary_output)
				possible_questions.add(binary_output)

			# limit amount of questions to be generated
			if len(possible_questions) >= limit:
				return possible_questions
		return possible_questions

	# check if generated question is valid
	def isValidQuestion(self, question):
		return question != None and len(question) > 0

generator = GenerateQuestions()
generator.generateQuestions(50)