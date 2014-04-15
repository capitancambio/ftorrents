from stevedore import extension
import logging
logger=logging.getLogger("ftorrents")

NAMESPACE="ftorrents.plugins"

def notify(titles):
        logger.debug("Broadcasting notifications")
        respones=new_extension_manager().map(callable,titles)
        for resp in respones:
                logger.info(resp)

def new_extension_manager():
        return extension.ExtensionManager(
                namespace= NAMESPACE,
                propagate_map_exceptions=False
            )


def callable(extension,titles):
        return extension.obj.notify(titles)

