from django.test import TestCase
from django.contrib.auth.models import User
from  chatgptapp.models import QuestionAnswer

class QuestionAnswerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a User object for testing
        cls.user = User.objects.create_user(username="testuser", password="testpassword")

    def setUp(self):
        # Create a QuestionAnswer object for each test case
        self.question_answer = QuestionAnswer.objects.create(
            question="What is the capital of France?",
            answer="The capital of France is Paris.",
            user=self.user,
        )

    def test_question_answer_creation(self):
        # Check if the QuestionAnswer object was created correctly
        self.assertEqual(self.question_answer.question, "What is the capital of France?")
        self.assertEqual(self.question_answer.answer, "The capital of France is Paris.")
        self.assertEqual(self.question_answer.user, self.user)

    def test_question_answer_str_method(self):
        # Check if the __str__ method returns the expected string representation
        expected_str = f"Question: What is the capital of France?, Answer: The capital of France is Paris."
        self.assertEqual(str(self.question_answer), expected_str)

    def test_question_answer_timestamp_auto_now_add(self):
        # Check if the timestamp field is automatically set to the current time when created
        self.assertIsNotNone(self.question_answer.timestamp)

    def test_question_answer_db_table_name(self):
        # Check if the database table name is set as expected
        self.assertEqual(QuestionAnswer._meta.db_table, 'QuestionAnswer')

