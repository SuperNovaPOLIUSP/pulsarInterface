import unittest
import sys
import os
sys.path.append('..')
sys.path.append('../..')
from pulsarInterface.Course import Course, CourseError
from django.conf import settings
from datetime import date
from tools.MySQLConnection import MySQLConnection


def get_value_from_dictionary_or_default(dictionary, key, default):
    """Returns the value if the dictionary has the key, or default if it
    hasn't"""
    return default if key not in dictionary else dictionary[key]


def insert_course_into_database(data_dict):
    """Receives a dictionary containing all the necessary data to insert a new
    course into the database. Default values are provided if the dictionary
    does not contain them"""
    cursor = MySQLConnection()
    id_course = get_value_from_dictionary_or_default(data_dict, 'id', None)
    name = get_value_from_dictionary_or_default(data_dict, 'name', '')
    abbreviation = get_value_from_dictionary_or_default(data_dict,
                                                        'abbreviation', '')
    course_code = get_value_from_dictionary_or_default(data_dict, 'code', '')
    start_date = get_value_from_dictionary_or_default(data_dict, 'start_date',
                                                      '0000-00-00')
    end_date = get_value_from_dictionary_or_default(data_dict, 'end_date',
                                                    '0000-00-00')
    insert_fields = '(idCourse, name, abbreviation, courseCode, startDate,\
            endDate)' if id_course is not None else '(name, abbreviation,\
            courseCode, startDate, endDate)'
    cursor.execute("INSERT INTO course " + insert_fields + " VALUES (" +
                   str(id_course) + ", '" + name + "', '" + abbreviation + "', '" +
                   course_code + "', '" + start_date + "', '" +
                   end_date + "')")


class MySQLConnectionTest(unittest.TestCase):

    def setUp(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'aeSupernova.settings'
        settings.DATABASES['supernova']['NAME'] = 'supernova_test'
        self.valid_attributes = {'code': 'MAC0000', 'name':
                                 'Course Name', 'start_date': '2000-01-01',
                                 'start_date_object': date(2000, 1, 1),
                                 'abbreviation': 'C. Name',
                                 'end_date': '2014-01-01',
                                 'id': 23}
        self.more_valid_attributes = {'code': 'MAT0000', 'name':
                                      'Course Different',
                                      'start_date': '2001-01-01',
                                      'abbreviation': 'C. Diff',
                                      'end_date': '2012-01-01',
                                      'id': 24}
        self.valid_attributes_to_store = {'code': 'MAE0002', 'name':
                                          'Course Name Stored',
                                          'start_date': '2002-01-01',
                                          'abbreviation': 'C. Name Stor.',
                                          'end_date': '2015-01-01',
                                          'id': 40}
        self.wrong_type_attributes = {'code': 1000, 'name': None,
                                      'start_date': object(),
                                      'abbreviation': [],
                                      'end_date': None}
        self.wrong_format_attributes = {'start_date': '2000-14-01',
                                        'end_date': '2013-01-32'}
        self.invalid_attributes = {'id': 10}
        self.id_courses_to_delete = []
        self.populate()

    def tearDown(self):
        self.unpopulate()

    def populate(self):
        insert_course_into_database(self.valid_attributes)
        insert_course_into_database(self.more_valid_attributes)
        self.id_courses_to_delete.append(self.valid_attributes['id'])
        self.id_courses_to_delete.append(self.more_valid_attributes['id'])

    def unpopulate(self):
        cursor = MySQLConnection()
        for id_course in self.id_courses_to_delete:
            cursor.execute('DELETE FROM course WHERE idCourse = ' +
                           str(id_course))

    def create_course_with_valid_attributes(self):
        return Course(self.valid_attributes['code'],
                      self.valid_attributes['name'],
                      self.valid_attributes['start_date'])

    def remove_temporary_course_with_id(self, idCourse):
        cursor = MySQLConnection()
        cursor.execute("DELETE FROM course WHERE idCourse = " + str(idCourse))

    def test_create_course_object(self):
        course = self.create_course_with_valid_attributes()
        self.assertIsNotNone(course)
        self.assertEqual(course.courseCode, self.valid_attributes['code'])
        self.assertEqual(course.name, self.valid_attributes['name'])
        self.assertEqual(course.startDate, self.valid_attributes['start_date'])

    def test_create_course_object_with_date_object(self):
        course = Course(self.valid_attributes['code'],
                        self.valid_attributes['name'],
                        self.valid_attributes['start_date_object'])
        self.assertIsNotNone(course)
        self.assertEqual(course.courseCode, self.valid_attributes['code'])
        self.assertEqual(course.name, self.valid_attributes['name'])
        self.assertEqual(course.startDate,
                         str(self.valid_attributes['start_date_object']))

    def test_raise_exception_on_creation_course_code(self):
        self.assertRaises(CourseError, Course,
                          self.wrong_type_attributes['code'],
                          self.valid_attributes['name'],
                          self.valid_attributes['start_date'])

    def test_raise_exception_on_creation_name(self):
        self.assertRaises(CourseError, Course,
                          self.valid_attributes['code'],
                          self.wrong_type_attributes['name'],
                          self.valid_attributes['start_date'])

    def test_raise_exception_on_creation_start_date(self):
        self.assertRaises(CourseError, Course,
                          self.valid_attributes['code'],
                          self.valid_attributes['name'],
                          self.wrong_type_attributes['start_date'])

    def test_course_equality(self):
        course1 = self.create_course_with_valid_attributes()
        course2 = self.create_course_with_valid_attributes()
        self.assertEqual(course1, course2)

    def test_course_inequality(self):
        course1 = self.create_course_with_valid_attributes()
        course2 = Course(self.valid_attributes['code'] + ' ',
                         self.valid_attributes['name'],
                         self.valid_attributes['start_date'])
        self.assertNotEqual(course1, course2)

    def test_equality_with_different_object_should_return_false(self):
        course1 = self.create_course_with_valid_attributes()
        course2 = course1.__dict__
        self.assertNotEqual(course1, course2)

    def test_set_abbreviation_with_valid_abbreviation(self):
        course = self.create_course_with_valid_attributes()
        course.setAbbreviation(self.valid_attributes['abbreviation'])

    def test_set_abbreviation_should_raise_if_not_a_string(self):
        course = self.create_course_with_valid_attributes()
        self.assertRaises(CourseError,
                          course.setAbbreviation,
                          self.wrong_type_attributes['abbreviation'])

    def test_set_end_date_with_correct_end_date(self):
        course = self.create_course_with_valid_attributes()
        course.setEndDate(self.valid_attributes['end_date'])
        self.assertEqual(course.endDate, self.valid_attributes['end_date'])

    def test_set_end_date_with_wrong_format(self):
        course = self.create_course_with_valid_attributes()
        self.assertRaises(CourseError,
                          course.setEndDate,
                          self.wrong_format_attributes['end_date'])

    def test_set_end_date_with_none(self):
        course = self.create_course_with_valid_attributes()
        course.setEndDate(self.wrong_type_attributes['end_date'])
        self.assertEqual(course.endDate, None)

    def test_pick_by_id(self):
        course1 = self.create_course_with_valid_attributes()
        course2 = Course.pickById(self.valid_attributes['id'])
        self.assertEqual(course1.name, course2.name)
        self.assertEqual(course1.courseCode, course2.courseCode)
        self.assertEqual(course1.startDate, course2.startDate)
        self.assertEqual(course2.abbreviation,
                         self.valid_attributes['abbreviation'])
        self.assertEqual(course2.endDate,
                         self.valid_attributes['end_date'])
        self.assertEqual(course2.idCourse, self.valid_attributes['id'])

    def test_pick_by_id_should_return_none_if_not_found(self):
        should_be_none = Course.pickById(self.invalid_attributes['id'])
        self.assertIsNone(should_be_none)

    def test_find_by_id_should_return_one_result(self):
        result = Course.find(idCourse=self.valid_attributes['id'])
        self.assertEqual(len(result), 1)

    def test_find_course_code_equal_should_return_one_result(self):
        result = Course.find(courseCode_equal=self.valid_attributes['code'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].courseCode, self.valid_attributes['code'])

    def test_find_course_code_like_should_return_more_than_one_result(self):
        result = Course.find(courseCode_like=self.valid_attributes['code'][3:])
        self.assertGreater(len(result), 1)
        for course in result:
            self.assertIn(self.valid_attributes['code'][3:], course.courseCode)

    def test_find_abbreviation_equal_should_return_one_result(self):
        result = Course.find(abbreviation_equal=
                             self.valid_attributes['abbreviation'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].abbreviation,
                         self.valid_attributes['abbreviation'])

    def test_find_abbreviation_like_should_return_more_than_one_result(self):
        result = Course.find(abbreviation_like=
                             self.valid_attributes['abbreviation'][:3])
        self.assertGreater(len(result), 1)
        for course in result:
            self.assertIn(self.valid_attributes['abbreviation'][:3],
                          course.abbreviation)

    def test_find_name_equal_should_return_one_result(self):
        result = Course.find(name_equal=self.valid_attributes['name'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, self.valid_attributes['name'])

    def test_find_name_like_should_return_more_than_one_result(self):
        result = Course.find(name_like=self.valid_attributes['name'][:5])
        self.assertGreater(len(result), 1)
        for course in result:
            self.assertIn(self.valid_attributes['name'][:5], course.name)

    def test_find_start_date_equal_should_return_one_result(self):
        result = Course.find(startDate_equal=
                             self.valid_attributes['start_date'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].startDate,
                         self.valid_attributes['start_date'])

    def test_find_start_date_like_should_return_more_than_one_result(self):
        result = Course.find(startDate_like=
                             self.valid_attributes['start_date'][4:])
        self.assertGreater(len(result), 1)
        for course in result:
            self.assertIn(self.valid_attributes['start_date'][4:],
                          course.startDate)

    def test_find_end_date_equal_should_return_one_result(self):
        result = Course.find(endDate_equal=
                             self.valid_attributes['end_date'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].endDate,
                         self.valid_attributes['end_date'])

    def test_find_end_date_like_should_return_more_than_one_result(self):
        result = Course.find(endDate_like=
                             self.valid_attributes['end_date'][4:])
        self.assertGreater(len(result), 1)
        for course in result:
            self.assertIn(self.valid_attributes['end_date'][4:],
                          course.endDate)

    def test_find_with_list_of_ids_should_return_more_than_one_result(self):
        ids_course = [self.valid_attributes['id'],
                      self.more_valid_attributes['id']]
        result = Course.find(idCourse=ids_course)
        self.assertGreater(len(result), 1)
        for course in result:
            self.assertIn(course.idCourse, ids_course)

    def test_storing_course(self):
        course = Course(self.valid_attributes_to_store['code'],
                        self.valid_attributes_to_store['name'],
                        self.valid_attributes_to_store['start_date'])
        course.store()
        self.assertIsNotNone(course.idCourse)
        self.id_courses_to_delete.append(course.idCourse)
        self.assertEqual(course, Course.pickById(course.idCourse))

    def test_storing_course_after_setting_end_date(self):
        course = Course(self.valid_attributes_to_store['code'],
                        self.valid_attributes_to_store['name'],
                        self.valid_attributes_to_store['start_date'])
        course.setEndDate(self.valid_attributes['end_date'])
        course.store()
        self.id_courses_to_delete.append(course.idCourse)
        course_in_bank = Course.pickById(course.idCourse)
        self.assertEqual(course_in_bank.endDate,
                         self.valid_attributes['end_date'])

    def test_store_course_twice_should_get_id_course_from_bank(self):
        course1 = Course(self.valid_attributes_to_store['code'],
                         self.valid_attributes_to_store['name'],
                         self.valid_attributes_to_store['start_date'])
        course2 = Course(self.valid_attributes_to_store['code'],
                         self.valid_attributes_to_store['name'],
                         self.valid_attributes_to_store['start_date'])
        course1.store()
        course2.store()
        self.assertIsNotNone(course2.idCourse)
        self.assertEqual(course1.idCourse, course2.idCourse)
        self.id_courses_to_delete.append(course1.idCourse)

    def test_updating_course(self):
        course = Course(self.valid_attributes_to_store['code'],
                        self.valid_attributes_to_store['name'],
                        self.valid_attributes_to_store['start_date'])
        course.store()
        self.id_courses_to_delete.append(course.idCourse)
        course.abbreviation = self.more_valid_attributes['abbreviation']
        course.store()
        course_in_bank = Course.pickById(course.idCourse)
        self.assertEqual(course_in_bank.abbreviation,
                         self.more_valid_attributes['abbreviation'])

    def test_deleting_course_with_valid_id(self):
        course = Course.pickById(self.valid_attributes['id'])
        self.id_courses_to_delete.remove(course.idCourse)
        course.delete()
        self.assertFalse(Course.pickById(self.valid_attributes['id']))

    def test_deleting_course_with_invalid_id(self):
        course = Course(self.valid_attributes_to_store['code'],
                        self.valid_attributes_to_store['name'],
                        self.valid_attributes_to_store['start_date'])
        course.idCourse = self.invalid_attributes['id']
        self.assertRaises(CourseError, course.delete)

    def test_deleting_course_without_id(self):
        course = Course(self.valid_attributes_to_store['code'],
                        self.valid_attributes_to_store['name'],
                        self.valid_attributes_to_store['start_date'])
        self.assertRaises(CourseError, course.delete)


if __name__ == '__main__':
    unittest.main()
