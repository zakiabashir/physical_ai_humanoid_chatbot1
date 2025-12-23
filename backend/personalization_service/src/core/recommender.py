"""
Recommendation engine for personalized content suggestions.

This module provides rule-based recommendations based on user progress.
"""

from typing import List, Dict, Any


class RecommendationEngine:
    """Rule-based recommendation engine for textbook chapters."""

    # Chapter dependencies and order
    CHAPTER_ORDER = [
        "intro",
        "chapter-01-foundations",
        "chapter-02-ros2",
        "chapter-03-gazebo",
        "chapter-04-isaac",
        "chapter-05-vla",
        "chapter-06-capstone"
    ]

    CHAPTER_TITLES = {
        "intro": "Introduction",
        "chapter-01-foundations": "Physical AI Foundations",
        "chapter-02-ros2": "ROS 2",
        "chapter-03-gazebo": "Gazebo & Digital Twins",
        "chapter-04-isaac": "NVIDIA Isaac",
        "chapter-05-vla": "Vision-Language-Action Models",
        "chapter-06-capstone": "Capstone Project"
    }

    def get_recommendations(
        self,
        user_progress: List[Dict[str, Any]],
        user_bookmarks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Get personalized chapter recommendations based on user progress.

        Args:
            user_progress: List of progress records for the user
            user_bookmarks: List of bookmarks for the user

        Returns:
            List of recommended chapters with reasons
        """
        recommendations = []
        completed_chapters = {p['chapter_id'] for p in user_progress if p['status'] == 'complete'}
        in_progress_chapters = {p['chapter_id'] for p in user_progress if p['status'] == 'in_progress'}
        bookmarked_chapters = {b['chapter_id'] for b in user_bookmarks}

        # Rule 1: Sequential recommendation (next chapter after last completed)
        last_completed_idx = -1
        for chapter_id in self.CHAPTER_ORDER:
            if chapter_id in completed_chapters:
                last_completed_idx = self.CHAPTER_ORDER.index(chapter_id)
            elif chapter_id in in_progress_chapters:
                last_completed_idx = self.CHAPTER_ORDER.index(chapter_id) - 1
                break

        if last_completed_idx >= 0 and last_completed_idx < len(self.CHAPTER_ORDER) - 1:
            next_chapter = self.CHAPTER_ORDER[last_completed_idx + 1]
            if next_chapter not in completed_chapters and next_chapter not in in_progress_chapters:
                recommendations.append({
                    "chapter_id": next_chapter,
                    "chapter_title": self.CHAPTER_TITLES.get(next_chapter, next_chapter),
                    "reason": "sequential",
                    "description": f"Continue to the next chapter in sequence: {self.CHAPTER_TITLES.get(next_chapter)}"
                })

        # Rule 2: Bookmarked chapters (suggest related content)
        for chapter_id in bookmarked_chapters:
            # Find related chapters (chapters around the bookmarked one)
            try:
                idx = self.CHAPTER_ORDER.index(chapter_id)
                # Suggest next chapter after bookmark
                if idx + 1 < len(self.CHAPTER_ORDER):
                    next_chapter = self.CHAPTER_ORDER[idx + 1]
                    if next_chapter not in completed_chapters:
                        recommendations.append({
                            "chapter_id": next_chapter,
                            "chapter_title": self.CHAPTER_TITLES.get(next_chapter),
                            "reason": "bookmark_based",
                            "description": f"Based on your bookmark in {self.CHAPTER_TITLES.get(chapter_id)}"
                        })
            except ValueError:
                continue

        # Rule 3: Foundational chapters for beginners
        if not completed_chapters and not in_progress_chapters:
            recommendations.append({
                "chapter_id": "chapter-01-foundations",
                "chapter_title": self.CHAPTER_TITLES["chapter-01-foundations"],
                "reason": "foundational",
                "description": "Start with the foundational concepts of Physical AI"
            })

        # Remove duplicates and limit to 3 recommendations
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec['chapter_id'] not in seen:
                unique_recommendations.append(rec)
                seen.add(rec['chapter_id'])
                if len(unique_recommendations) >= 3:
                    break

        return unique_recommendations
