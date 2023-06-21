import unittest
import os
import sys
currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(currentDir, '../sample'))
from getAllUserNames import updateUserList as updateUL


class testUpdateUserList(unittest.TestCase):

    def testNewFile(self):
        userList = ['a','b','c']
        filePath = "temp.csv"
        if os.path.exists(filePath):
            os.remove(filePath)
        self.assertEqual(os.path.exists(filePath),False)
        df = updateUL(['a','b','c'],filePath)
        self.assertEqual(os.path.exists(filePath),True)
        os.remove(filePath)
        self.assertEqual(os.path.exists(filePath),False)
        self.assertEqual(df["User"].to_list(),userList)

    def testExistingFile(self):
        userList = ['a','b','c']
        filePath = "temp.csv"
        if os.path.exists(filePath):
            os.remove(filePath,filePath)
        self.assertEqual(os.path.exists(filePath),False)
        updateUL(['a','b','c'],filePath)
        df = updateUL(['a','d','e'],filePath)
        self.assertEqual(df["User"].to_list(),['a','b','c','d','e'])
        os.remove(filePath)
        

# Executar os testes
if __name__ == '__main__':
    unittest.main()
