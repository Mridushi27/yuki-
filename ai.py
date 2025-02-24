"""
Machine Learning model simulation for disease risk prediction.
"""
from typing import Dict, Any, Tuple
import numpy as np
from .config import RISK_THRESHOLDS, HEALTH_METRICS
from .utils import logger

class HealthRiskPredictor:
    def __init__(self):
        self.risk_thresholds = RISK_THRESHOLDS
        self.health_metrics = HEALTH_METRICS

    def predict_diabetes_risk(self, health_data: Dict[str, Any]) -> Tuple[float, str]:
        """
        Simulate diabetes risk prediction based on blood glucose and other factors.
        Returns risk score and recommendation.
        """
        try:
            # Extract relevant metrics
            glucose = float(health_data.get('blood_glucose', 0))
            bmi = float(health_data.get('bmi', 0))
            age = int(health_data.get('age', 0))
            
            # Simple risk calculation (this is a simulation)
            base_risk = 0.0
            
            # Blood glucose contribution
            if glucose > 126:  # Fasting blood glucose
                base_risk += 0.4
            elif glucose > 100:
                base_risk += 0.2
                
            # BMI contribution
            if bmi > 30:
                base_risk += 0.3
            elif bmi > 25:
                base_risk += 0.15
                
            # Age contribution
            if age > 45:
                base_risk += 0.2
            elif age > 35:
                base_risk += 0.1
                
            # Normalize risk score
            risk_score = min(1.0, base_risk)
            
            # Generate recommendation
            if risk_score >= self.risk_thresholds['diabetes']['high']:
                recommendation = "High risk of diabetes. Please consult a healthcare provider and consider taking a HbA1c test."
            elif risk_score >= self.risk_thresholds['diabetes']['medium']:
                recommendation = "Moderate risk of diabetes. Monitor blood glucose levels and maintain a healthy lifestyle."
            else:
                recommendation = "Low risk of diabetes. Continue maintaining a healthy lifestyle."
                
            return risk_score, recommendation
            
        except Exception as e:
            logger.error(f"Error in diabetes risk prediction: {str(e)}")
            return 0.0, "Unable to calculate diabetes risk due to invalid data."

    def predict_hypertension_risk(self, health_data: Dict[str, Any]) -> Tuple[float, str]:
        """
        Simulate hypertension risk prediction based on blood pressure and other factors.
        Returns risk score and recommendation.
        """
        try:
            # Extract relevant metrics
            systolic = float(health_data.get('systolic_bp', 0))
            diastolic = float(health_data.get('diastolic_bp', 0))
            heart_rate = float(health_data.get('heart_rate', 0))
            
            # Simple risk calculation (this is a simulation)
            base_risk = 0.0
            
            # Blood pressure contribution
            if systolic >= 140 or diastolic >= 90:
                base_risk += 0.4
            elif systolic >= 130 or diastolic >= 80:
                base_risk += 0.2
                
            # Heart rate contribution
            if heart_rate > 100:
                base_risk += 0.2
            elif heart_rate > 90:
                base_risk += 0.1
                
            # Normalize risk score
            risk_score = min(1.0, base_risk)
            
            # Generate recommendation
            if risk_score >= self.risk_thresholds['hypertension']['high']:
                recommendation = "High risk of hypertension. Please consult a healthcare provider and monitor blood pressure regularly."
            elif risk_score >= self.risk_thresholds['hypertension']['medium']:
                recommendation = "Moderate risk of hypertension. Consider lifestyle changes and regular blood pressure monitoring."
            else:
                recommendation = "Low risk of hypertension. Maintain healthy lifestyle habits."
                
            return risk_score, recommendation
            
        except Exception as e:
            logger.error(f"Error in hypertension risk prediction: {str(e)}")
            return 0.0, "Unable to calculate hypertension risk due to invalid data."

    def predict_risk(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main prediction function that assesses multiple health risks.
        """
        try:
            diabetes_risk, diabetes_recommendation = self.predict_diabetes_risk(health_data)
            hypertension_risk, hypertension_recommendation = self.predict_hypertension_risk(health_data)
            
            return {
                "diabetes": {
                    "risk_score": round(diabetes_risk * 100, 1),
                    "recommendation": diabetes_recommendation
                },
                "hypertension": {
                    "risk_score": round(hypertension_risk * 100, 1),
                    "recommendation": hypertension_recommendation
                }
            }
            
        except Exception as e:
            logger.error(f"Error in risk prediction: {str(e)}")
            return {
                "error": "Unable to calculate health risks. Please ensure all required data is provided correctly."
            }

# Initialize the predictor
risk_predictor = HealthRiskPredictor()
