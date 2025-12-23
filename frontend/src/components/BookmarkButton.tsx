/**
 * BookmarkButton Component
 *
 * Add/remove bookmarks for chapters and sections
 */

import React, { useState, useEffect } from 'react';
import { personalizationApi, Bookmark } from '../lib/api';

interface BookmarkButtonProps {
  chapterId: string;
  sectionId?: string;
}

export default function BookmarkButton({ chapterId, sectionId }: BookmarkButtonProps): React.JSX.Element {
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    checkBookmark();
  }, [chapterId, sectionId]);

  const checkBookmark = async () => {
    try {
      const bookmarks = await personalizationApi.getBookmarks();
      const exists = bookmarks.some(
        b => b.chapter_id === chapterId && (!sectionId || b.section_id === sectionId)
      );
      setIsBookmarked(exists);
    } catch {
      // User not authenticated or error
      setIsBookmarked(false);
    }
  };

  const toggleBookmark = async () => {
    setIsLoading(true);
    try {
      if (isBookmarked) {
        // Find and delete bookmark
        const bookmarks = await personalizationApi.getBookmarks();
        const bookmark = bookmarks.find(
          b => b.chapter_id === chapterId && (!sectionId || b.section_id === sectionId)
        );
        if (bookmark) {
          await personalizationApi.deleteBookmark(bookmark.id);
        }
      } else {
        await personalizationApi.createBookmark(chapterId, sectionId || '');
      }
      setIsBookmarked(!isBookmarked);
    } catch (err) {
      console.error('Bookmark error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={toggleBookmark}
      disabled={isLoading}
      className={`bookmark-btn ${isBookmarked ? 'bookmarked' : ''}`}
      aria-label={isBookmarked ? 'Remove bookmark' : 'Add bookmark'}
      title={isBookmarked ? 'Remove bookmark' : 'Add bookmark'}
    >
      <svg
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill={isBookmarked ? 'currentColor' : 'none'}
        stroke="currentColor"
        strokeWidth="2"
      >
        <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
      </svg>
    </button>
  );
}
