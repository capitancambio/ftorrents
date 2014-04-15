import unittest
from mock import patch
import mock
import logging
import notifier
from stevedore import extension
#avoid logs during unittesting
logging.disable(logging.CRITICAL)

class NotifierTests(unittest.TestCase):

        @patch("stevedore.extension")
        def test_callable(self,ext):
                ext.obj.notify.return_value="ok"
                res=notifier.callable(ext,[])
                self.assertEquals("ok",res,"Callable was called")

        def test_new_extension_manager(self):
               mgr=notifier.new_extension_manager() 
               self.assertEquals(notifier.NAMESPACE,mgr.namespace,"namespace is correct")
               self.assertEquals(False,mgr.propagate_map_exceptions,"we want to ignore the exceptions")

        @patch("ftorrents.notifier.new_extension_manager")
        def test_notify(self,factory):
                ext1=mock.Mock()
                ext2=mock.Mock()
                #two extensions
                ext1.notify.return_value=1
                ext2.notify.return_value=2
                #fake instance
                mgr=extension.ExtensionManager("TEST")
                #this is super dirty, but! well....
                mgr.extensions=[extension.Extension("name1","","",ext1),extension.Extension("namer2","","",ext2)]
                
                factory.return_value=mgr
                #titles to notify
                titles=['title1','title2']
                #notify
                notifier.notify(titles)
                #make sure all the pluggins were notified
                ext1.notify.assert_called_once_with(titles)
                ext2.notify.assert_called_once_with(titles)
        
