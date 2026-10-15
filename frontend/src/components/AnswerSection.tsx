import React from 'react';

interface AnswerSectionProps {
  answer: string;
  isCorrected?: boolean;
}

export const AnswerSection: React.FC<AnswerSectionProps> = ({ answer, isCorrected }) => {
  return (
    <div className="answer-section card">
      <h3 className="section-title">ANSWER</h3>
      <p className="answer-text">
        {answer}
      </p>
      {isCorrected && (
        <div className="correction-notice">
          Answer refined after evidence review
        </div>
      )}
    </div>
  );
};
