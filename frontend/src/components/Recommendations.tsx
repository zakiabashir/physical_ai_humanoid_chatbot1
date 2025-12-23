/**
 * Recommendations Component
 *
 * Personalized content recommendations based on user progress
 */

import React, { useState, useEffect } from 'react';
import { personalizationApi, Recommendation } from '../lib/api';

export default function Recommendations(): React.JSX.Element | null {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadRecommendations();
  }, []);

  const loadRecommendations = async () => {
    try {
      const data = await personalizationApi.getRecommendations();
      setRecommendations(data);
    } catch {
      setRecommendations([]);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <div className="recommendations loading">Loading recommendations...</div>;
  }

  if (recommendations.length === 0) {
    return null;
  }

  return (
    <div className="recommendations">
      <h3>Recommended for You</h3>
      <ul className="recommendations-list">
        {recommendations.map((rec, idx) => (
          <li key={idx} className="recommendation-item">
            <a href={`/docs/${rec.chapter_id}`}>
              <span className="rec-title">{rec.title}</span>
              <span className="rec-reason">{rec.reason}</span>
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
