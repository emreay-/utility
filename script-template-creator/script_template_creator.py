import os
import argparse


def create_directory_if_not_exists(directory: str):
    if not os.path.isdir(directory):
        os.mkdir(directory)


class ScriptTemplateCreator(object):

    def __init__(self, output_dir: str, name: str, is_no_test: bool = False):
        self.output_dir = output_dir
        self.name = name
        self.is_no_test = is_no_test

    def handle_output_dir(self):
        pass
    
    def handle_test_dir(self):
        pass
    
    def create_init_py_if_not_exists(self):
        pass

    def generate_template_script_str(self):
        pass
    
    def generate_test_script_str(self):
        pass
    
    def create_template_script(self):
        pass

    def create_test_script(self):
        pass

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
    pass