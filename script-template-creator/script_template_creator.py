import os
import argparse


def create_directory_if_not_exists(directory: str):
    if not os.path.isdir(directory):
        os.mkdir(directory)

def create_file(path: str):
    open(path, 'a').close()


def make_module_name_in_class_name_format(input: str) -> str:
    return ''.join([i.title() for i in input.split('_')])


class ScriptTemplateCreator(object):

    def __init__(self, output_dir: str, name: str, is_no_test: bool = False):
        self.output_dir = output_dir
        self.name = name
        self.is_no_test = is_no_test
        self.test_dir = os.path.join(self.output_dir, 'test')
        self.template_file_path = os.path.join(self.output_dir, '{}.py'.format(self.name))
        self.test_file_path = os.path.join(self.test_dir, 'test_{}.py'.format(self.name))
        self.class_name = make_module_name_in_class_name_format(self.name)

    def handle_output_dir(self):
        create_directory_if_not_exists(self.output_dir)
    
    def handle_test_dir(self):
        create_directory_if_not_exists(self.test_dir)
    
    def create_init_py_if_not_exists(self):
        _init_py_path = os.path.join(self.output_dir, '__init__.py')
        if not os.path.exists(_init_py_path):
            create_file(_init_py_path)

    def generate_template_script_str(self) -> str:
        return '''import os
import argparse


class {}(object):

    def __init__(self):
        pass


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input', required=True)
    parser.add_argument('-o', '--output_dir', help='Output', required=True)
    parser.add_argument('-F', '--flag', help='Flag', action='store_true')
    args = parser.parse_args()

    return args.input, args.output_dir, args.flag


if __name__ == '__main__':
    input, output_dir, flag = parse_arguments()
'''.format(self.class_name)
    
    def generate_test_script_str(self) -> str:
        return '''import os
import sys
import unittest
import tempfile
import shutil

current_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_path, os.pardir))
sys.path.insert(0, parent_dir)

import {}


class {}(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()
    '''.format(self.name, self.class_name + 'Tests')
    
    def create_template_script(self):
        with open(self.template_file_path, 'w') as template:
            template.writelines(self.generate_template_script_str())

    def create_test_script(self):
        with open(self.test_file_path, 'w') as test:
            test.writelines(self.generate_test_script_str())

    def run(self):
        self.handle_output_dir()
        self.create_init_py_if_not_exists()
        self.create_template_script()
        if not self.is_no_test:
            self.handle_test_dir()
            self.create_test_script()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_dir', help='Output directory for the created template', required=True)
    parser.add_argument('-N', '--name', help='Module name', required=True)
    parser.add_argument('--no_test', help='Do not create test file template', action='store_true')
    args = parser.parse_args()

    return args.output_dir, args.name, args.no_test

if __name__ == '__main__':
    output_dir, name, no_test = parse_arguments()
    creator = ScriptTemplateCreator(output_dir, name, no_test)
    creator.run()