import os
import sys
import unittest
import tempfile
import shutil

current_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_path, os.pardir))
sys.path.insert(0, parent_dir)

from script_template_creator import create_directory_if_not_exists, ScriptTemplateCreator, \
make_module_name_in_class_name_format


def remove_dir_if_exists(*args):
    for directory in args:
        if os.path.isdir(directory):
            shutil.rmtree(directory)


def get_random_directory(delete=False):
    dir_name = tempfile.mkdtemp()
    if delete:
        remove_dir_if_exists(dir_name)
    return dir_name


class Handlers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.__random_dir = get_random_directory(delete=True)
        cls.__output_dir = get_random_directory(delete=True)
        cls.__test_dir = os.path.join(cls.__output_dir, 'test')
        cls.__creator_object = ScriptTemplateCreator(output_dir=cls.__output_dir, 
                                                     name='amazing_module')
        cls.__init_py_path = os.path.join(cls.__output_dir, '__init__.py')

    @classmethod
    def tearDownClass(cls):
        remove_dir_if_exists(cls.__random_dir, cls.__output_dir)

    def test_create_directory_if_not_exists(self):
        self.assertFalse(os.path.isdir(self.__random_dir))
        create_directory_if_not_exists(self.__random_dir)
        self.assertTrue(os.path.isdir(self.__random_dir))
    
    def test_handle_output_dir(self):
        self.assertFalse(os.path.isdir(self.__output_dir))
        self.__creator_object.handle_output_dir()
        self.assertTrue(os.path.isdir(self.__output_dir))
    
    def test_handle_test_dir(self):
        self.assertFalse(os.path.isdir(self.__test_dir))
        self.__creator_object.handle_test_dir()
        self.assertTrue(os.path.isdir(self.__test_dir))


class InitPyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.__output_dir = get_random_directory(delete=True)
        cls.__creator_object = ScriptTemplateCreator(output_dir=cls.__output_dir, 
                                                     name='amazing_module')
        cls.__init_py_path = os.path.join(cls.__output_dir, '__init__.py')
        cls.__creator_object.handle_output_dir()

    @classmethod
    def tearDownClass(cls):
        remove_dir_if_exists(cls.__output_dir)

    def test_create_init_py_if_not_exists(self):
        self.assertFalse(os.path.exists(self.__init_py_path))
        self.__creator_object.create_init_py_if_not_exists()
        self.assertTrue(os.path.exists(self.__init_py_path))


class StringGenerators(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.__output_dir = get_random_directory(delete=True)
        cls.__name = 'amazing_module'
        cls.__creator_object = ScriptTemplateCreator(output_dir=cls.__output_dir, 
                                                     name=cls.__name)
        cls.__expected_class_name_str = 'AmazingModule'                                                    
        cls.__expected_template_str = '''import os
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
'''.format(cls.__expected_class_name_str)

        cls.__expected_test_str = '''import os
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
    '''.format(cls.__name, cls.__expected_class_name_str + 'Tests')

    @classmethod
    def tearDownClass(cls):
        remove_dir_if_exists(cls.__output_dir)

    def test_make_module_name_in_class_name_format(self):
        _class_name_str = make_module_name_in_class_name_format(self.__creator_object.name)
        self.assertEqual(_class_name_str, self.__expected_class_name_str)

    def test_generate_template_script_str(self):
        _template_str = self.__creator_object.generate_template_script_str()
        self.assertEqual(_template_str, self.__expected_template_str)
    
    def test_generate_test_script_str(self):
        _test_str = self.__creator_object.generate_test_script_str()
        self.assertEqual(_test_str, self.__expected_test_str)


class CreatingTemplates(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.__output_dir = get_random_directory(delete=True)
        cls.__name = 'amazing_module'
        cls.__test_dir = os.path.join(cls.__output_dir, 'test')
        cls.__creator_object = ScriptTemplateCreator(output_dir=cls.__output_dir, 
                                                     name=cls.__name)
        cls.__creator_object.handle_output_dir()
        cls.__creator_object.handle_test_dir()
        cls.__template_script_path = os.path.join(cls.__output_dir, cls.__name + '.py')
        cls.__test_script_path = os.path.join(cls.__test_dir, 'test_{}.py'.format(cls.__name))

    @classmethod
    def tearDownClass(cls):
        remove_dir_if_exists(cls.__output_dir)

    def test_create_template_script(self):
        self.assertFalse(os.path.exists(self.__template_script_path))
        self.__creator_object.create_template_script()
        self.assertTrue(os.path.exists(self.__template_script_path))
    
    def test_create_test_script(self):
        self.assertFalse(os.path.exists(self.__test_script_path))
        self.__creator_object.create_test_script()
        self.assertTrue(os.path.exists(self.__test_script_path))


if __name__ == '__main__':
    unittest.main()