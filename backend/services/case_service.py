"""
Case Service - Business logic for case management
Handles filtering, sorting, and statistics calculation
"""

from typing import List, Dict, Any, Tuple


class CaseService:
    """Service for case-related business logic"""
    
    @staticmethod
    def filter_cases_by_status(cases: List[Any], status_filter: str) -> List[Any]:
        """
        Filter cases by status
        
        Args:
            cases: List of case objects
            status_filter: "All", "Not Found", or "Found"
            
        Returns:
            Filtered list of cases
        """
        if status_filter == "Not Found":
            return [c for c in cases if c.status == "NF"]
        elif status_filter == "Found":
            return [c for c in cases if c.status == "F"]
        else:
            return cases
    
    @staticmethod
    def filter_registered_cases_by_search(cases: List[Any], search_term: str) -> List[Any]:
        """
        Filter registered cases by search term
        
        Args:
            cases: List of registered case objects
            search_term: Search string
            
        Returns:
            Filtered list of cases
        """
        if not search_term:
            return cases
        
        search_lower = search_term.lower()
        return [
            c for c in cases
            if search_lower in c.name.lower()
            or (c.city and search_lower in c.city.lower())
        ]
    
    @staticmethod
    def filter_public_cases_by_search(cases: List[Any], search_term: str) -> List[Any]:
        """
        Filter public submission cases by search term
        
        Args:
            cases: List of public submission objects
            search_term: Search string
            
        Returns:
            Filtered list of cases
        """
        if not search_term:
            return cases
        
        search_lower = search_term.lower()
        return [
            c for c in cases
            if search_lower in (c.location or "").lower()
            or (hasattr(c, 'city') and c.city and search_lower in c.city.lower())
            or search_lower in (c.submitted_by or "").lower()
        ]
    
    @staticmethod
    def sort_cases_by_date(cases: List[Any], reverse: bool = True) -> List[Any]:
        """
        Sort cases by submission date
        
        Args:
            cases: List of case objects
            reverse: If True, newest first (default)
            
        Returns:
            Sorted list of cases
        """
        try:
            return sorted(cases, key=lambda x: x.submitted_on, reverse=reverse)
        except:
            return cases
    
    @staticmethod
    def sort_public_cases_by_date(cases: List[Any], reverse: bool = True) -> List[Any]:
        """
        Sort public submission cases by submission date
        
        Args:
            cases: List of public submission objects
            reverse: If True, newest first (default)
            
        Returns:
            Sorted list of cases
        """
        try:
            return sorted(
                cases, 
                key=lambda x: x.submitted_on if hasattr(x, 'submitted_on') else '', 
                reverse=reverse
            )
        except:
            return cases
    
    @staticmethod
    def calculate_statistics(registered_cases: List[Any], public_submissions: List[Any]) -> Dict[str, int]:
        """
        Calculate case statistics
        
        Args:
            registered_cases: List of registered cases
            public_submissions: List of public submissions
            
        Returns:
            Dictionary with statistics
        """
        total_cases = len(registered_cases) + len(public_submissions)
        
        found_count = (
            len([c for c in registered_cases if c.status == 'F']) +
            len([c for c in public_submissions if c.status == 'F'])
        )
        
        not_found_count = (
            len([c for c in registered_cases if c.status == 'NF']) +
            len([c for c in public_submissions if c.status == 'NF'])
        )
        
        return {
            'total_cases': total_cases,
            'found_count': found_count,
            'not_found_count': not_found_count,
            'admin_count': len(registered_cases),
            'public_count': len(public_submissions)
        }
    
    @staticmethod
    def get_status_display(status: str) -> Tuple[str, str]:
        """
        Get status emoji and text
        
        Args:
            status: Status code ("F" or "NF")
            
        Returns:
            Tuple of (emoji, text)
        """
        if status == "F":
            return "🟢", "FOUND"
        else:
            return "🔴", "NOT FOUND"


# Global instance
case_service = CaseService()
