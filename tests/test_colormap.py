# Copyright (c) 2020,Vienna University of Technology,
# Department of Geodesy and Geoinformation
# All rights reserved.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL VIENNA UNIVERSITY OF TECHNOLOGY, DEPARTMENT OF
# GEODESY AND GEOINFORMATION BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""
Tests for the ColorMap().
"""
import os
import shutil
import unittest
import random
import matplotlib.pyplot as plt
import gdal
from src.colorella.colormap import ColorMap
from src.colorella.utils import cptfile2dict, gdal2dict, json2list
import matplotlib.colors as col


class TestColormap(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        test_path = r'test_data'
        test_output = r'test_output'
        os.chdir(test_path)
        if not os.path.exists(test_output):
            os.makedirs(test_output)

    def setUp(self):
        """ Create random test data and set up path """
        self.test_path = r'test_data'
        self.test_output = r'test_output'
        cm_list = plt.colormaps()
        self.default_cm = random.choice(cm_list)

        red = [(0., 1, 1), (1, 0, 0)]
        green = [(0., 1, 1), (1, 0, 0)]
        blue = [(0., 1, 1), (1, 0, 0)]
        alpha = [(0., 1, 1), (1, 0, 0)]
        for i in range(4):
            red.append((random.uniform(0, 1), random.randint(0, 1), random.randint(0, 1)))
            green.append((random.uniform(0, 1), random.randint(0, 1), random.randint(0, 1)))
            blue.append((random.uniform(0, 1), random.randint(0, 1), random.randint(0, 1)))
            alpha.append((random.uniform(0, 1), random.randint(0, 1), random.randint(0, 1)))
        red.sort(key=lambda x: x[0])
        green.sort(key=lambda x: x[0])
        blue.sort(key=lambda x: x[0])
        alpha.sort(key=lambda x: x[0])
        self.cdict = {'red': tuple(red), 'green': tuple(green), 'blue': tuple(blue), 'alpha': tuple(alpha)}

        self.clist = []
        for i in range(random.randint(1, 20)):
            self.clist.append((random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))
        print('Present DIR is : ', os.getcwd())

    def tearDown(self):
        """ Removes all test data. """

        shutil.rmtree(self.test_output)
        os.chdir(self.test_path)

    def test_cmap_from_name(self):
        """
        Tests creation of a ColorMap from mpl name
        """
        cmap = ColorMap(self.default_cm)
        self.assertIsInstance(cmap, ColorMap)

    def test_cmap_from_dict(self):
        """
        Tests creation of a ColorMap from a dictionary
        """
        cmap = ColorMap(self.cdict)
        self.assertIsInstance(cmap, ColorMap)

    def test_cmap_from_list(self):
        """
        Tests creation of a ColorMap from a list
        """
        cmap = ColorMap(self.clist)
        self.assertIsInstance(cmap, ColorMap)

    def test_cmap_from_gdal(self):
        """
        Tests creation of a ColorMap from a gdal ct file
        """
        ct_file = 'sgrt_ct_cont_ssm.ct.cpt'
        cmap = ColorMap().from_gdal(ct_file)
        self.assertIsInstance(cmap, ColorMap)

    def test_cmap_from_cpt(self):
        """
        Tests creation of a ColorMap from a matplotlib ColorMap file
        """
        cpt_file = 'ETOPO1.cpt'
        cmap = ColorMap().from_cptfile(cpt_file)
        self.assertIsInstance(cmap, ColorMap)

    def test_cmap_from_json(self):
        """
        Tests creation of a ColorMap from a json file
        """
        json_file = 'Rainbow.json'
        cmap = ColorMap().from_json(json_file)
        self.assertIsInstance(cmap, ColorMap)

    def test_listed2segmented(self):
        """
        Tests conversion from a Listed ColorMap to a LinearSegmented ColorMap
        """
        cmap = ColorMap(self.clist)
        cmap = cmap.to_gradient()
        self.assertIsInstance(cmap, col.LinearSegmentedColormap)

    def test_save(self):
        """
        Tests save ColorMap as cpt file
        """
        cmap_write = ColorMap(self.clist)
        cmap_write.save_as_cpt(self.test_output)
        cmap_read = ColorMap(self.test_output)
        self.assertEqual(cmap_read, cmap_write)

    def test_convert2greyscale(self):
        """
        Tests conversion to a greyscale ColorMap
        """
        cmap = ColorMap(self.default_cm)
        cmap_grey = cmap.convert2greyscale()
        cmap_grey.view()
        self.assertIsInstance(cmap_grey, col.LinearSegmentedColorMap)

    def test_to_matplotlib(self):
        """
        Tests creation of a matplotlib ColorMap object
        """
        cmap = ColorMap(self.default_cm)
        self.assertIsInstance(cmap, col.LinearSegmentedColorMap)

    def test_to_dict(self):
        """
        Tests writing ColorMap colors to dictionary
        """
        cmap = ColorMap(self.cdict)
        cdict_out = cmap.to_dict()
        self.assertEqual(self.cdict, cdict_out)

    def test_to_list(self):
        """
        Tests writing ColorMap colors to list
        """
        cmap = ColorMap(self.clist)
        clist_out = cmap.to_list()
        self.assertListEqual(self.clist, clist_out)

    def test_reverse(self):
        """
        Tests reversing ColorMap colors

        """
        cmap = ColorMap(self.cdict)
        colors_reverse = []
        keys = []

        for key in cmap._segmentdata:
            keys.append(key)
            channel = cmap._segmentdata[key]
            data = []

            for c in channel:
                data.append((1 - c[0], c[2], c[1]))
            colors_reverse.append(sorted(data))

        self.assertEqual(self.cdict, colors_reverse)

    def test_view(self):
        """
        Tests ploting the ColorMap
        """
        cmap = ColorMap(self.default_cm)
        cmap.view()

    def test_to_gdal(self):
        """
        Tests converting the matplotlib ColorMap to a gdal color table
        """
        cmap = ColorMap(self.default_cm)
        g_ct = cmap.to_gdal()
        self.assertIsInstance(g_ct, gdal.ColorTable)


if __name__ == '__main__':
    unittest.main()