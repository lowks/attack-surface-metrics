__author__ = 'kevin'

import unittest
from attack_surface.stack import Stack
from attack_surface.call import Call
from attack_surface.call_graph import CallGraph


class StackTestCase(unittest.TestCase):

    def test_push(self):
        # Arrange
        test_stack = Stack()

        # Act
        test_stack.push(1)
        test_stack.push(2)

        # Assert
        self.assertEqual(len(test_stack), 2)

    def test_pop(self):
        # Arrange
        test_stack = Stack()

        # Act
        test_stack.push(1)
        test_stack.push(2)

        popped_value = test_stack.pop()

        # Assert
        self.assertEqual(popped_value, 2)
        self.assertEqual(len(test_stack), 1)

    def test_top(self):
        # Arrange
        test_stack = Stack()

        # Act
        test_stack.push(1)
        test_stack.push(2)

        # Assert
        self.assertEqual(test_stack.top, 2)


class CallTestCase(unittest.TestCase):

    def test_identity_function_name(self):
        # Arrange
        cflow_line = "printf()"
        test_call = Call(cflow_line)

        # Assert
        self.assertEqual(test_call.identity, "printf()")

    def test_identity_full(self):
        # Arrange
        cflow_line = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call = Call(cflow_line)

        # Assert
        self.assertEqual(test_call.identity, "xstrdup()<char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89>")

    def test_function_name_only_name(self):
        # Arrange
        cflow_line = "printf()"
        test_call = Call(cflow_line)

        # Assert
        self.assertEqual(test_call.function_name, "printf()")

    def test_function_name_full(self):
        # Arrange
        cflow_line = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call = Call(cflow_line)

        # Assert
        self.assertEqual(test_call.function_name, "xstrdup()")

    def test_function_signature_only_name(self):
        # Arrange
        cflow_line = "printf()"
        test_call = Call(cflow_line)

        # Assert
        self.assertIsNone(test_call.function_signature)

    def test_function_signature_full(self):
        # Arrange
        cflow_line = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call = Call(cflow_line)

        # Assert
        self.assertEqual(test_call.function_signature, "<char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89>")

    def test_is_leaf(self):
        # Arrange
        cflow_line = "printf()"
        test_call = Call(cflow_line)

        # Assert
        self.assertTrue(test_call.is_leaf())

    def test_is_not_leaf(self):
        # Arrange
        cflow_line = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call = Call(cflow_line)

        # Assert
        self.assertFalse(test_call.is_leaf())

    def test_is_input_function(self):
        # Arrange
        cflow_line = "getchar()"
        test_call = Call(cflow_line)

        # Assert
        self.assertTrue(test_call.is_input_function())

    def test_is_not_input_function(self):
        # Arrange
        cflow_line = "printf()"
        test_call = Call(cflow_line)

        # Assert
        self.assertFalse(test_call.is_input_function())

    def test_is_not_input_function_no_leaf(self):
        # Arrange
        cflow_line = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call = Call(cflow_line)

        # Assert
        self.assertFalse(test_call.is_input_function())

    def test_is_output_function(self):
        # Arrange
        cflow_line = "printf()"
        test_call = Call(cflow_line)

        # Assert
        self.assertTrue(test_call.is_output_function())

    def test_is_not_output_function(self):
        # Arrange
        cflow_line = "getchar()"
        test_call = Call(cflow_line)

        # Assert
        self.assertFalse(test_call.is_output_function())

    def test_is_not_output_function_no_leaf(self):
        # Arrange
        cflow_line = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call = Call(cflow_line)

        # Assert
        self.assertFalse(test_call.is_output_function())

    def test_equal(self):
        # Arrange
        cflow_line = "getchar()"
        test_call_1 = Call(cflow_line)
        test_call_2 = Call(cflow_line)

        # Assert
        self.assertEqual(test_call_1, test_call_2)

    def test_not_equal(self):
        # Arrange
        cflow_line_1 = "getchar()"
        cflow_line_2 = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call_1 = Call(cflow_line_1)
        test_call_2 = Call(cflow_line_2)

        # Assert
        self.assertNotEqual(test_call_1, test_call_2)


class CallGraphTestCase(unittest.TestCase):

    def test_entry_points_count(self):
        # Arrange
        test_call_graph = CallGraph("./helloworld")

        # Act
        entry_points_count = len(test_call_graph.entry_points)

        # Assert
        self.assertEqual(entry_points_count, 1)

    def test_exit_points_count(self):
        # Arrange
        test_call_graph = CallGraph("./helloworld/")

        # Act
        exit_points_count = len(test_call_graph.exit_points)

        # Assert
        self.assertEqual(exit_points_count, 4)

    def test_entry_points_content(self):
        # Arrange
        test_call_graph = CallGraph("./helloworld")
        expected_content = [Call("    greet_b() <void greet_b (int i) at ./src/helloworld.c:34>:")]

        # Act
        all_entry_points_encountered = all([c in test_call_graph.entry_points for c in expected_content])

        # Assert
        self.assertTrue(all_entry_points_encountered)


    def test_exit_points_content(self):
        # Arrange
        test_call_graph = CallGraph("./helloworld")
        expected_content = [Call("            recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"),
                            Call("        recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"),
                            Call("main() <int main (void) at ./src/helloworld.c:18>:"),
                            Call("        greet() <void greet (int greeting_code) at ./src/greetings.c:14>:")]

        # Act
        all_exit_points_encountered = all([c in test_call_graph.exit_points for c in expected_content])

        # Assert
        self.assertTrue(all_exit_points_encountered)


if __name__ == '__main__':
    unittest.main()

