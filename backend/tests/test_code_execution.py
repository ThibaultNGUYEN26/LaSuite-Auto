import unittest
from unittest.mock import patch

from services.code_execution import run_python_code


class CodeExecutionEncodingTests(unittest.TestCase):
    def test_python_output_uses_utf8_for_accents_and_bom(self):
        result = run_python_code("print('\\ufeffÉvolution de la surface pâturale')")

        self.assertEqual(result["exit_code"], 0)
        self.assertEqual(result["stderr"], "")
        self.assertEqual(result["stdout"], "\ufeffÉvolution de la surface pâturale\n")

    @patch("services.code_execution.subprocess.run")
    def test_subprocess_receives_explicit_utf8_configuration(self, run):
        run.return_value.stdout = "résultat"
        run.return_value.stderr = ""
        run.return_value.returncode = 0

        result = run_python_code("print('résultat')")

        request = run.call_args.kwargs
        self.assertEqual(request["encoding"], "utf-8")
        self.assertEqual(request["errors"], "replace")
        self.assertEqual(request["env"]["PYTHONUTF8"], "1")
        self.assertEqual(request["env"]["PYTHONIOENCODING"], "utf-8")
        self.assertEqual(result["stdout"], "résultat")


if __name__ == "__main__":
    unittest.main()
