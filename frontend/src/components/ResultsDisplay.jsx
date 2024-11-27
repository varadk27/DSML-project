import React from 'react';
import { Progress } from '@/components/ui/progress';

const ResultsDisplay = ({ results }) => {
  if (!results) return null;

  return (
    <div className="bg-white rounded-lg shadow p-6 space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-2">Overall Match Score</h3>
        <div className="flex items-center gap-2">
          <Progress value={results.match_score} className="w-full" />
          <span className="text-sm font-medium">{results.match_score}%</span>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-2">Skills Analysis</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {results.skills_match.map((skill, index) => (
            <div key={index} className="bg-gray-50 p-3 rounded">
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">{skill.name}</span>
                <span className="text-sm text-gray-600">{skill.match_score}%</span>
              </div>
              <Progress value={skill.match_score} className="w-full" />
            </div>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-2">Experience Analysis</h3>
        <p className="text-gray-700">{results.experience_analysis}</p>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-2">Recommendations</h3>
        <ul className="list-disc pl-5 space-y-2">
          {results.recommendations.map((rec, index) => (
            <li key={index} className="text-gray-700">{rec}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ResultsDisplay;