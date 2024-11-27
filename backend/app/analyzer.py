# backend/app/analyzer.py
import pdfplumber
from transformers import pipeline
import numpy as np
from typing import List, Dict, Any
import spacy
import re

class ResumeAnalyzer:
    def __init__(self):
        # Initialize NLP models
        self.skill_classifier = pipeline("zero-shot-classification")
        self.nlp = spacy.load("en_core_web_sm")
        self.text_classifier = pipeline("text-classification")

    def extract_text_from_pdf(self, file) -> str:
        """Extract text content from uploaded PDF file."""
        text = ""
        try:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
        return text

    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess extracted text."""
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s\-\.]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections from the resume."""
        sections = {
            'experience': '',
            'education': '',
            'skills': '',
            'projects': ''
        }
        
        current_section = ''
        lines = text.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            if any(section in line_lower for section in sections.keys()):
                current_section = next(
                    section for section in sections.keys() 
                    if section in line_lower
                )
            elif current_section:
                sections[current_section] += line + '\n'
                
        return sections

    def analyze_skills(self, text: str, required_skills: List[str]) -> List[Dict]:
        """Analyze skills mentioned in the resume against required skills."""
        results = self.skill_classifier(
            text,
            required_skills,
            multi_label=True
        )
        
        skills_match = []
        for skill, score in zip(results['labels'], results['scores']):
            skills_match.append({
                'name': skill,
                'match_score': round(score * 100, 2)
            })
        
        return sorted(skills_match, key=lambda x: x['match_score'], reverse=True)

    def analyze_experience(self, text: str, required_exp: Dict) -> Dict[str, Any]:
        """Analyze professional experience against job requirements."""
        sections = self.extract_sections(text)
        exp_text = sections['experience']
        
        # Extract years of experience
        year_patterns = [
            r'(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?',
            r'(\d+)\+?\s*y\.?e\.?'
        ]
        years = []
        for pattern in year_patterns:
            matches = re.findall(pattern, exp_text.lower())
            years.extend([int(y) for y in matches])
        
        total_years = max(years) if years else 0
        
        # Analyze relevance of experience
        relevance_score = self.text_classifier(exp_text)[0]['score']
        
        # Calculate final experience score
        exp_score = min(
            (total_years / required_exp['years']) * 100,
            100
        ) if total_years > 0 else 0
        
        final_score = (exp_score + (relevance_score * 100)) / 2
        
        return {
            'score': round(final_score, 2),
            'years': total_years,
            'relevance': round(relevance_score * 100, 2),
            'analysis': self._generate_experience_analysis(final_score, total_years, required_exp)
        }

    def _generate_experience_analysis(self, score: float, years: int, required_exp: Dict) -> str:
        """Generate detailed experience analysis text."""
        if score >= 85:
            analysis = "Excellent experience match! "
        elif score >= 70:
            analysis = "Good experience match. "
        else:
            analysis = "Experience could be better aligned. "
            
        if years >= required_exp['years']:
            analysis += f"Has {years} years of experience (meets requirement of {required_exp['years']} years). "
        else:
            analysis += f"Has {years} years of experience (below requirement of {required_exp['years']} years). "
            
        return analysis.strip()

    def generate_recommendations(self, skills_match: List[Dict], exp_analysis: Dict) -> List[str]:
        """Generate personalized recommendations based on analysis."""
        recommendations = []
        
        # Skills recommendations
        weak_skills = [skill for skill in skills_match if skill['match_score'] < 70]
        if weak_skills:
            skills_str = ", ".join([s['name'] for s in weak_skills])
            recommendations.append(f"Consider strengthening skills in: {skills_str}")
            
        # Experience recommendations
        if exp_analysis['score'] < 70:
            recommendations.append(
                "Focus on gaining more relevant experience in key areas"
            )
        
        # Add general recommendations if needed
        if not recommendations:
            recommendations.append(
                "Strong profile! Consider highlighting leadership experience and quantitative achievements"
            )
            
        return recommendations

    def analyze_resume(self, resume_text: str, job_config: Dict) -> Dict[str, Any]:
        """Perform complete resume analysis."""
        # Preprocess text
        cleaned_text = self.preprocess_text(resume_text)
        
        # Analyze skills
        skills_match = self.analyze_skills(
            cleaned_text,
            job_config['required_skills']
        )
        
        # Analyze experience
        experience_analysis = self.analyze_experience(
            cleaned_text,
            job_config['required_experience']
        )
        
        # Generate recommendations
        recommendations = self.generate_recommendations(
            skills_match,
            experience_analysis
        )
        
        # Calculate overall match score
        skills_score = np.mean([skill['match_score'] for skill in skills_match])
        match_score = round(
            (skills_score + experience_analysis['score']) / 2,
            2
        )
        
        return {
            "match_score": match_score,
            "skills_match": skills_match,
            "experience_analysis": experience_analysis,
            "recommendations": recommendations
        }