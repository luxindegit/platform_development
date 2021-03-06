#!/usr/bin/env python3

from __future__ import print_function

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

from compat import StringIO
from vndk_definition_tool import (ELF, ELFLinker, PT_SYSTEM, PT_VENDOR,
                                  GenericRefs)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TESTDATA_DIR = os.path.join(SCRIPT_DIR ,'testdata', 'test_vndk')


class ELFLinkerVNDKTest(unittest.TestCase):
    def _get_paths_from_nodes(self, nodes):
        return sorted([node.path for node in nodes])

    def test_compute_vndk(self):
        class MockBannedLibs(object):
            def is_banned(self, name):
                return False

        input_dir = os.path.join(TESTDATA_DIR, 'pre_treble')

        graph = ELFLinker.create_from_dump(
                system_dirs=[os.path.join(input_dir, 'system')],
                vendor_dirs=[os.path.join(input_dir, 'vendor')])

        vndk = graph.compute_vndk(sp_hals=set(), vndk_stable=set(),
                                  vndk_customized_for_system=set(),
                                  vndk_customized_for_vendor=set(),
                                  generic_refs=None,
                                  banned_libs=MockBannedLibs())

        self.assertEqual(['/system/lib/libcutils.so',
                          '/system/lib64/libcutils.so'],
                         self._get_paths_from_nodes(vndk.vndk_core))
        self.assertEqual([], self._get_paths_from_nodes(vndk.vndk_fwk_ext))
        self.assertEqual([], self._get_paths_from_nodes(vndk.vndk_vnd_ext))

    def test_compute_vndk_fwk_ext(self):
        class MockBannedLibs(object):
            def is_banned(self, name):
                return False

        generic_refs_dir = os.path.join(TESTDATA_DIR, 'vndk_ext_ref')

        generic_refs = GenericRefs.create_from_dir(generic_refs_dir)

        input_dir = os.path.join(TESTDATA_DIR, 'vndk_fwk_ext')

        graph = ELFLinker.create_from_dump(
                system_dirs=[os.path.join(input_dir, 'system')],
                vendor_dirs=[os.path.join(input_dir, 'vendor')],
                generic_refs=generic_refs)

        vndk = graph.compute_vndk(sp_hals=set(), vndk_stable=set(),
                                  vndk_customized_for_system=set(),
                                  vndk_customized_for_vendor=set(),
                                  generic_refs=generic_refs,
                                  banned_libs=MockBannedLibs())

        self.assertEqual(['/system/lib/vndk/libRS.so',
                          '/system/lib/vndk/libcutils.so',
                          '/system/lib64/vndk/libRS.so',
                          '/system/lib64/vndk/libcutils.so'],
                         self._get_paths_from_nodes(vndk.vndk_core))
        self.assertEqual(['/system/lib/libRS.so',
                          '/system/lib64/libRS.so'],
                         self._get_paths_from_nodes(vndk.vndk_fwk_ext))
        self.assertEqual([], self._get_paths_from_nodes(vndk.vndk_vnd_ext))

    def test_compute_vndk_vnd_ext(self):
        class MockBannedLibs(object):
            def is_banned(self, name):
                return False

        generic_refs_dir = os.path.join(TESTDATA_DIR, 'vndk_ext_ref')

        generic_refs = GenericRefs.create_from_dir(generic_refs_dir)

        input_dir = os.path.join(TESTDATA_DIR, 'vndk_vnd_ext')

        graph = ELFLinker.create_from_dump(
                system_dirs=[os.path.join(input_dir, 'system')],
                vendor_dirs=[os.path.join(input_dir, 'vendor')],
                generic_refs=generic_refs)

        vndk = graph.compute_vndk(sp_hals=set(), vndk_stable=set(),
                                  vndk_customized_for_system=set(),
                                  vndk_customized_for_vendor=set(),
                                  generic_refs=generic_refs,
                                  banned_libs=MockBannedLibs())

        self.assertEqual(['/system/lib/vndk/libRS.so',
                          '/system/lib/vndk/libcutils.so',
                          '/system/lib64/vndk/libRS.so',
                          '/system/lib64/vndk/libcutils.so'],
                         self._get_paths_from_nodes(vndk.vndk_core))
        self.assertEqual([], self._get_paths_from_nodes(vndk.vndk_fwk_ext))
        self.assertEqual(['/system/lib/libRS.so', '/system/lib64/libRS.so'],
                         self._get_paths_from_nodes(vndk.vndk_vnd_ext))


if __name__ == '__main__':
    unittest.main()
