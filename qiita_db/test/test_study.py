from unittest import TestCase, main
from datetime import date

from future.utils import viewitems

from qiita_core.exceptions import IncompetentQiitaDeveloperError
from qiita_core.util import qiita_test_checker
from qiita_db.base import QiitaObject
from qiita_db.study import Study, StudyPerson
from qiita_db.investigation import Investigation
from qiita_db.user import User
from qiita_db.exceptions import QiitaDBColumnError, QiitaDBStatusError

# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------


@qiita_test_checker()
class TestStudyPerson(TestCase):
    def setUp(self):
        self.studyperson = StudyPerson(1)

    def test_create_studyperson(self):
        new = StudyPerson.create('SomeDude', 'somedude@foo.bar',
                                 '111 fake street', '111-121-1313')
        self.assertEqual(new.id, 4)
        obs = self.conn_handler.execute_fetchall(
            "SELECT * FROM qiita.study_person WHERE study_person_id = 4")
        self.assertEqual(obs, [[4, 'SomeDude', 'somedude@foo.bar',
                         '111 fake street', '111-121-1313']])

    def test_create_studyperson_already_exists(self):
        obs = StudyPerson.create('LabDude', 'lab_dude@foo.bar')
        self.assertEqual(obs.name, 'LabDude')
        self.assertEqual(obs.email, 'lab_dude@foo.bar')

    def test_retrieve_name(self):
        self.assertEqual(self.studyperson.name, 'LabDude')

    def test_set_name_fail(self):
        with self.assertRaises(AttributeError):
            self.studyperson.name = 'Fail Dude'

    def test_retrieve_email(self):
        self.assertEqual(self.studyperson.email, 'lab_dude@foo.bar')

    def test_set_email_fail(self):
        with self.assertRaises(AttributeError):
            self.studyperson.email = 'faildude@foo.bar'

    def test_retrieve_address(self):
        self.assertEqual(self.studyperson.address, '123 lab street')

    def test_retrieve_address_null(self):
        person = StudyPerson(2)
        self.assertEqual(person.address, None)

    def test_set_address(self):
        self.studyperson.address = '123 nonsense road'
        self.assertEqual(self.studyperson.address, '123 nonsense road')

    def test_retrieve_phone(self):
        self.assertEqual(self.studyperson.phone, '121-222-3333')

    def test_retrieve_phone_null(self):
        person = StudyPerson(3)
        self.assertEqual(person.phone, None)

    def test_set_phone(self):
        self.studyperson.phone = '111111111111111111121'
        self.assertEqual(self.studyperson.phone, '111111111111111111121')


@qiita_test_checker()
class TestStudy(TestCase):
    def setUp(self):
        self.study = Study(1)

        self.info = {
            "timeseries_type_id": 1,
            "metadata_complete": True,
            "mixs_compliant": True,
            "number_samples_collected": 25,
            "number_samples_promised": 28,
            "portal_type_id": 3,
            "study_alias": "FCM",
            "study_description": "Microbiome of people who eat nothing but "
                                 "fried chicken",
            "study_abstract": "Exploring how a high fat diet changes the "
                              "gut microbiome",
            "emp_person_id": StudyPerson(2),
            "principal_investigator_id": StudyPerson(3),
            "lab_person_id": StudyPerson(1)
        }

        self.infoexp = {
            "timeseries_type_id": 1,
            "metadata_complete": True,
            "mixs_compliant": True,
            "number_samples_collected": 25,
            "number_samples_promised": 28,
            "portal_type_id": 3,
            "study_alias": "FCM",
            "study_description": "Microbiome of people who eat nothing but "
                                 "fried chicken",
            "study_abstract": "Exploring how a high fat diet changes the "
                              "gut microbiome",
            "emp_person_id": 2,
            "principal_investigator_id": 3,
            "lab_person_id": 1
        }

        self.existingexp = {
            'mixs_compliant': True,
            'metadata_complete': True,
            'reprocess': False,
            'number_samples_promised': 27,
            'emp_person_id': StudyPerson(2),
            'funding': None,
            'vamps_id': None,
            'first_contact': '2014-05-19 16:10',
            'principal_investigator_id': StudyPerson(3),
            'timeseries_type_id': 1,
            'study_abstract':
                "This is a preliminary study to examine the "
                "microbiota associated with the Cannabis plant. Soils samples "
                "from the bulk soil, soil associated with the roots, and the "
                "rhizosphere were extracted and the DNA sequenced. Roots "
                "from three independent plants of different strains were "
                "examined. These roots were obtained November 11, 2011 from "
                "plants that had been harvested in the summer. Future "
                "studies will attempt to analyze the soils and rhizospheres "
                "from the same location at different time points in the plant "
                "lifecycle.",
            'spatial_series': False,
            'study_description': 'Analysis of the Cannabis Plant Microbiome',
            'portal_type_id': 2,
            'study_alias': 'Cannabis Soils',
            'most_recent_contact': '2014-05-19 16:11',
            'lab_person_id': StudyPerson(1),
            'number_samples_collected': 27}

    def test_get_public(self):
        new = Study.create(User('test@foo.bar'), 'Identification of the '
                           'Microbiomes for Cannabis Soils', [1], self.info)
        obs = Study.get_public()
        self.assertEqual(obs, [Study(1)])

    def test_create_study_min_data(self):
        """Insert a study into the database"""
        obs = Study.create(User('test@foo.bar'), "Fried chicken microbiome",
                           [1], self.info)
        self.assertEqual(obs.id, 2)
        exp = {'mixs_compliant': True, 'metadata_complete': True,
               'reprocess': False, 'study_status_id': 1,
               'number_samples_promised': 28, 'emp_person_id': 2,
               'funding': None, 'vamps_id': None,
               'first_contact': date.today().isoformat(),
               'principal_investigator_id': 3,
               'timeseries_type_id': 1,
               'study_abstract': 'Exploring how a high fat diet changes the '
                                 'gut microbiome',
               'email': 'test@foo.bar', 'spatial_series': None,
               'study_description': 'Microbiome of people who eat nothing but'
                                    ' fried chicken',
               'portal_type_id': 3, 'study_alias': 'FCM', 'study_id': 2,
               'most_recent_contact': None, 'lab_person_id': 1,
               'study_title': 'Fried chicken microbiome',
               'number_samples_collected': 25}

        obsins = self.conn_handler.execute_fetchall(
            "SELECT * FROM qiita.study WHERE study_id = 2")
        self.assertEqual(len(obsins), 1)
        obsins = dict(obsins[0])
        self.assertEqual(obsins, exp)

        # make sure EFO went in to table correctly
        efo = self.conn_handler.execute_fetchall(
            "SELECT efo_id FROM qiita.study_experimental_factor "
            "WHERE study_id = 2")
        self.assertEqual(efo, [[1]])

    def test_create_study_with_investigation(self):
        """Insert a study into the database with an investigation"""
        obs = Study.create(User('test@foo.bar'), "Fried chicken microbiome",
                           [1], self.info, Investigation(1))
        self.assertEqual(obs.id, 2)
        # check the investigation was assigned
        obs = self.conn_handler.execute_fetchall(
            "SELECT * from qiita.investigation_study WHERE study_id = 2")
        self.assertEqual(obs, [[1, 2]])

    def test_create_study_all_data(self):
        """Insert a study into the database with every info field"""
        self.info.update({
            'vamps_id': 'MBE_1111111',
            'funding': 'FundAgency',
            'spatial_series': True,
            'metadata_complete': False,
            'reprocess': True,
            'first_contact': "Today"
            })
        obs = Study.create(User('test@foo.bar'), "Fried chicken microbiome",
                           [1], self.info)
        self.assertEqual(obs.id, 2)
        exp = {'mixs_compliant': True, 'metadata_complete': False,
               'reprocess': True, 'study_status_id': 1,
               'number_samples_promised': 28, 'emp_person_id': 2,
               'funding': 'FundAgency', 'vamps_id': 'MBE_1111111',
               'first_contact': "Today",
               'principal_investigator_id': 3, 'timeseries_type_id': 1,
               'study_abstract': 'Exploring how a high fat diet changes the '
                                 'gut microbiome',
               'email': 'test@foo.bar', 'spatial_series': True,
               'study_description': 'Microbiome of people who eat nothing '
                                    'but fried chicken',
               'portal_type_id': 3, 'study_alias': 'FCM', 'study_id': 2,
               'most_recent_contact': None, 'lab_person_id': 1,
               'study_title': 'Fried chicken microbiome',
               'number_samples_collected': 25}
        obsins = self.conn_handler.execute_fetchall(
            "SELECT * FROM qiita.study WHERE study_id = 2")
        self.assertEqual(len(obsins), 1)
        obsins = dict(obsins[0])
        self.assertEqual(obsins, exp)

        # make sure EFO went in to table correctly
        obsefo = self.conn_handler.execute_fetchall(
            "SELECT efo_id FROM qiita.study_experimental_factor "
            "WHERE study_id = 2")
        self.assertEqual(obsefo, [[1]])

    def test_create_missing_required(self):
        """ Insert a study that is missing a required info key"""
        self.info.pop("study_alias")
        with self.assertRaises(QiitaDBColumnError):
            Study.create(User('test@foo.bar'), "Fried Chicken Microbiome",
                         [1], self.info)

    def test_create_empty_efo(self):
        """ Insert a study that is missing a required info key"""
        with self.assertRaises(IncompetentQiitaDeveloperError):
            Study.create(User('test@foo.bar'), "Fried Chicken Microbiome",
                         [], self.info)

    def test_create_study_with_not_allowed_key(self):
        """Insert a study with key from _non_info present"""
        self.info.update({"study_id": 1})
        with self.assertRaises(QiitaDBColumnError):
            Study.create(User('test@foo.bar'), "Fried Chicken Microbiome",
                         [1], self.info)

    def test_create_unknown_db_col(self):
        """ Insert a study with an info key not in the database"""
        self.info["SHOULDNOTBEHERE"] = "BWAHAHAHAHAHA"
        with self.assertRaises(QiitaDBColumnError):
            Study.create(User('test@foo.bar'), "Fried Chicken Microbiome",
                         [1], self.info)

    def test_retrieve_title(self):
        self.assertEqual(self.study.title, 'Identification of the Microbiomes'
                         ' for Cannabis Soils')

    def test_set_title(self):
        new = Study.create(User('test@foo.bar'), 'Identification of the '
                           'Microbiomes for Cannabis Soils', [1], self.info)
        new.title = "Cannabis soils"
        self.assertEqual(new.title, "Cannabis soils")

    def test_set_title_public(self):
        """Tests for fail if editing title of a public study"""
        with self.assertRaises(QiitaDBStatusError):
            self.study.title = "FAILBOAT"

    def test_get_efo(self):
        self.assertEqual(self.study.efo, [1])

    def test_set_efo(self):
        """Set efo with list efo_id"""
        new = Study.create(User('test@foo.bar'), 'Identification of the '
                           'Microbiomes for Cannabis Soils', [1], self.info)
        new.efo = [3, 4]
        self.assertEqual(new.efo, [3, 4])

    def test_set_efo_empty(self):
        """Set efo with list efo_id"""
        new = Study.create(User('test@foo.bar'), 'Identification of the '
                           'Microbiomes for Cannabis Soils', [1], self.info)
        with self.assertRaises(IncompetentQiitaDeveloperError):
            new.efo = []

    def test_set_efo_public(self):
        """Set efo on a public study"""
        with self.assertRaises(QiitaDBStatusError):
            self.study.efo = 6

    def test_retrieve_info(self):
        for key, val in viewitems(self.existingexp):
            if isinstance(val, QiitaObject):
                self.existingexp[key] = val.id
        self.assertEqual(self.study.info, self.existingexp)

    def test_set_info(self):
        """Set info in a study"""
        newinfo = {
            "timeseries_type_id": 2,
            "metadata_complete": False,
            "number_samples_collected": 28,
            "lab_person_id": StudyPerson(2),
            "vamps_id": 'MBE_111222',
            "first_contact": "June 11, 2014"
        }
        new = Study.create(User('test@foo.bar'), 'Identification of the '
                           'Microbiomes for Cannabis Soils', [1], self.info)
        self.infoexp.update(newinfo)
        new.info = newinfo
        # add missing table cols
        self.infoexp["funding"] = None
        self.infoexp["spatial_series"] = None
        self.infoexp["most_recent_contact"] = None
        self.infoexp["reprocess"] = False
        self.infoexp["lab_person_id"] = 2
        self.assertEqual(new.info, self.infoexp)

    def test_set_info_public(self):
        """Tests for fail if editing info of a public study"""
        with self.assertRaises(QiitaDBStatusError):
            self.study.info = {"vamps_id": "12321312"}

    def test_set_info_disallowed_keys(self):
        """Tests for fail if sending non-info keys in info dict"""
        new = Study.create(User('test@foo.bar'), 'Identification of the '
                           'Microbiomes for Cannabis Soils', [1], self.info)
        with self.assertRaises(QiitaDBColumnError):
            new.info = {"email": "fail@fail.com"}

    def test_info_empty(self):
        new = Study.create(User('test@foo.bar'), 'Identification of the '
                           'Microbiomes for Cannabis Soils', [1], self.info)
        with self.assertRaises(IncompetentQiitaDeveloperError):
            new.info = {}

    def test_retrieve_status(self):
        self.assertEqual(self.study.status, "public")

    def test_set_status(self):
        new = Study.create(User('test@foo.bar'), 'Identification of the '
                           'Microbiomes for Cannabis Soils', [1], self.info)
        new.status = "private"
        self.assertEqual(new.status, "private")

    def test_retrieve_shared_with(self):
        self.assertEqual(self.study.shared_with, ['shared@foo.bar',
                         'demo@microbio.me'])

    def test_retrieve_pmids(self):
        exp = ['123456', '7891011']
        self.assertEqual(self.study.pmids, exp)

    def test_retrieve_pmids_empty(self):
        new = Study.create(User('test@foo.bar'), 'Identification of the '
                           'Microbiomes for Cannabis Soils', [1], self.info)
        self.assertEqual(new.pmids, [])

    def test_retrieve_investigation(self):
        self.assertEqual(self.study.investigation, 1)

    def test_retrieve_investigation_empty(self):
        new = Study.create(User('test@foo.bar'), 'Identification of the '
                           'Microbiomes for Cannabis Soils', [1], self.info)
        self.assertEqual(new.investigation, None)

    def test_retrieve_sample_template(self):
        self.assertEqual(self.study.sample_template, 1)

    def test_retrieve_data_types(self):
        self.assertEqual(self.study.data_types, ['18S'])

    def test_retrieve_data_types_none(self):
        new = Study.create(User('test@foo.bar'), 'Identification of the '
                           'Microbiomes for Cannabis Soils', [1], self.info)
        self.assertEqual(new.data_types, [])

    def test_retrieve_raw_data(self):
        self.assertEqual(self.study.raw_data, [1, 2])

    def test_retrieve_raw_data_none(self):
        new = Study.create(User('test@foo.bar'), 'Identification of the '
                           'Microbiomes for Cannabis Soils', [1], self.info)
        self.assertEqual(new.raw_data, [])

    def test_retrieve_preprocessed_data(self):
        self.assertEqual(self.study.preprocessed_data, [1, 2])

    def test_retrieve_preprocessed_data_none(self):
        new = Study.create(User('test@foo.bar'), 'Identification of the '
                           'Microbiomes for Cannabis Soils', [1], self.info)
        self.assertEqual(new.preprocessed_data, [])

    def test_retrieve_processed_data(self):
        self.assertEqual(self.study.processed_data, [1])

    def test_retrieve_processed_data_none(self):
        new = Study.create(User('test@foo.bar'), 'Identification of the '
                           'Microbiomes for Cannabis Soils', [1], self.info)
        self.assertEqual(new.processed_data, [])

    def test_add_pmid(self):
        self.study.add_pmid('4544444')
        exp = ['123456', '7891011', '4544444']
        self.assertEqual(self.study.pmids, exp)


if __name__ == "__main__":
    main()
