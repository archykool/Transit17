from .subway import SubwayService
from .lirr import LIRRService
from .mnr import MNRService

class MTAServiceFactory:
    """MTA service factory class"""
    
    @staticmethod
    def get_service(service_type):
        """
        get specified type of MTA service
        
        Args:
            service_type (str): service type,可选值：
                - 'subway': subway service
                - 'lirr': long island railroad service
                - 'mnr': metropolitan north railroad service
                
        Returns:
            BaseMTAService: corresponding service instance
        """
        services = {
            'subway': SubwayService,
            'lirr': LIRRService,
            'mnr': MNRService
        }
        
        service_class = services.get(service_type.lower())
        if not service_class:
            raise ValueError(f"Invalid service type: {service_type}")
            
        return service_class()
        
    @staticmethod
    def get_all_services():
        """get all available MTA services"""
        return {
            'subway': SubwayService(),
            'lirr': LIRRService(),
            'mnr': MNRService()
        } 