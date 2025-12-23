/**
 * ProgressBar Component
 *
 * Displays reading progress across all chapters
 */

import React, { useState, useEffect } from 'react';
import { personalizationApi, ProgressRecord } from '../lib/api';

export default function ProgressBar(): React.JSX.Element {
  const [progress, setProgress] = useState<ProgressRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      const data = await personalizationApi.getProgress();
      setProgress(data);
    } catch {
      // User not authenticated
      setProgress([]);
    } finally {
      setIsLoading(false);
    }
  };

  // Calculate completion percentage
  const totalChapters = 7; // 6 chapters + intro
  const completedChapters = progress.filter(p => p.status === 'completed').length;
  const percentage = Math.round((completedChapters / totalChapters) * 100);

  if (isLoading) {
    return <div className="progress-bar loading"></div>;
  }

  if (progress.length === 0) {
    return null; // Don't show for anonymous users
  }

  return (
    <div className="progress-bar-container">
      <div className="progress-header">
        <span className="progress-label">Your Progress</span>
        <span className="progress-percentage">{percentage}%</span>
      </div>
      <div className="progress-track">
        <div className="progress-fill" style={{ width: `${percentage}%` }}></div>
      </div>
      <div className="progress-chapters">
        {Array.from({ length: totalChapters }).map((_, idx) => {
          const chapterId = idx === 0 ? 'intro' : `chapter-${String(idx).padStart(2, '0')}`;
          const chapterProgress = progress.find(p => p.chapter_id === chapterId);
          const status = chapterProgress?.status || 'not_started';

          return (
            <div
              key={chapterId}
              className={`chapter-dot ${status}`}
              title={`Chapter ${idx}: ${status.replace('_', ' ')}`}
            ></div>
          );
        })}
      </div>
    </div>
  );
}
