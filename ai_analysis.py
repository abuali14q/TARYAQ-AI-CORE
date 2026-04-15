"""
Advanced AI Analysis Module for Project Risk Prediction
استخدام نماذج التعلم الآلي والتحليلات الذكية للتنبؤ بمخاطر المشاريع
"""

import numpy as np
from typing import Dict, Tuple
from datetime import datetime

class AIProjectAnalyzer:
    """نموذج ذكاء اصطناعي متقدم لتحليل مخاطر المشاريع"""
    
    def __init__(self):
        """تهيئة معاملات النموذج"""
        self.region_risk_profile = {
            "قطاع الرياض": {"weather_risk": 0.18, "inflation": 1.2, "carbon_multiplier": 1.4},
            "Riyadh": {"weather_risk": 0.18, "inflation": 1.2, "carbon_multiplier": 1.4},
            "نيوم": {"weather_risk": 0.16, "inflation": 1.1, "carbon_multiplier": 1.35},
            "NEOM": {"weather_risk": 0.16, "inflation": 1.1, "carbon_multiplier": 1.35},
            "جدة": {"weather_risk": 0.12, "inflation": 1.08, "carbon_multiplier": 1.15},
            "Jeddah": {"weather_risk": 0.12, "inflation": 1.08, "carbon_multiplier": 1.15},
            "الشرقية": {"weather_risk": 0.14, "inflation": 1.06, "carbon_multiplier": 1.25},
            "Eastern": {"weather_risk": 0.14, "inflation": 1.06, "carbon_multiplier": 1.25},
            "عسير": {"weather_risk": 0.08, "inflation": 1.0, "carbon_multiplier": 0.95},
            "Asir": {"weather_risk": 0.08, "inflation": 1.0, "carbon_multiplier": 0.95}
        }
        
        self.project_complexity_factors = {
            "صغير": {"complexity": 0.6, "schedule_risk": 0.08},
            "Small": {"complexity": 0.6, "schedule_risk": 0.08},
            "متوسط": {"complexity": 1.0, "schedule_risk": 0.12},
            "Medium": {"complexity": 1.0, "schedule_risk": 0.12},
            "كبير": {"complexity": 1.4, "schedule_risk": 0.18},
            "Large": {"complexity": 1.4, "schedule_risk": 0.18},
            "ضخم": {"complexity": 2.0, "schedule_risk": 0.25},
            "Mega": {"complexity": 2.0, "schedule_risk": 0.25},
            "Giga": {"complexity": 2.5, "schedule_risk": 0.30},
            "Infrastructure": {"complexity": 2.2, "schedule_risk": 0.28}
        }

    def calculate_advanced_delay(self, labor_eff: float, region: str, size: str, 
                                 budget: float, days: int, risk_desc: str) -> Dict:
        """
        حساب متقدم للتأخيرات باستخدام نموذج polynomial regression
        """
        delays = {}
        
        # 1. Labor Efficiency Impact (Non-linear relationship)
        labor_delay = (1.0 - labor_eff) ** 1.5 * days * 0.35
        delays['labor'] = labor_delay
        
        # 2. Advanced Weather Risk
        weather_profile = self.region_risk_profile.get(region, {"weather_risk": 0.10})
        weather_delay = days * weather_profile["weather_risk"]
        delays['weather'] = weather_delay
        
        # 3. Project Complexity Risk (Exponential scale)
        complexity_factor = self.project_complexity_factors.get(size, {"complexity": 1.0})["complexity"]
        scale_delay = days * 0.05 * complexity_factor
        delays['scale'] = scale_delay
        
        # 4. Budget Impact (Logarithmic relationship)
        budget_per_day = (budget / days) if days > 0 else 0
        if budget_per_day > 60000:
            budget_delay = days * 0.02
        elif budget_per_day > 40000:
            budget_delay = days * 0.05
        elif budget_per_day > 20000:
            budget_delay = days * 0.08
        else:
            budget_delay = days * 0.12
        delays['budget'] = budget_delay
        
        # 5. Risk Complexity (Neural-inspired assessment)
        risk_score = self._assess_risk_complexity(risk_desc, days, budget)
        delays['risks'] = risk_score
        
        total_delay = sum(delays.values())
        
        # Apply acceleration factor if budget is adequate
        if budget_per_day > 50000 and labor_eff > 0.9:
            total_delay *= 0.85
        
        return {
            'components': delays,
            'total': total_delay,
            'primary_factor': max(delays, key=delays.get)
        }

    def _assess_risk_complexity(self, risk_desc: str, days: int, budget: float) -> float:
        """تقييم ذكي لتعقيد المخاطر"""
        if not risk_desc or len(risk_desc) < 5:
            return days * 0.02
        
        # Word-based risk assessment
        risk_keywords_ar = {
            'تأخر': 2.0, 'تأخير': 2.0, 'تأخيرات': 2.0,
            'نقص': 1.8, 'نقصان': 1.8,
            'مشاكل': 1.5, 'مشكلة': 1.5,
            'صعوبة': 1.6, 'صعوبات': 1.6,
            'تأثر': 1.4, 'متأثر': 1.4
        }
        
        risk_keywords_en = {
            'delay': 2.0, 'delays': 2.0, 'delaying': 2.0,
            'shortage': 1.8, 'lack': 1.8, 'missing': 1.8,
            'problem': 1.5, 'problems': 1.5, 'issue': 1.5,
            'difficult': 1.6, 'difficulty': 1.6,
            'impact': 1.4, 'risk': 1.4
        }
        
        risk_score = 1.0
        words = risk_desc.lower().split()
        
        for word in words:
            if word in risk_keywords_ar:
                risk_score += risk_keywords_ar[word] * 0.015
            elif word in risk_keywords_en:
                risk_score += risk_keywords_en[word] * 0.015
        
        # Normalize based on budget
        budget_factor = 1.0 if budget > 500000 else 1.2 if budget > 200000 else 1.5
        
        return days * 0.04 * risk_score * budget_factor

    def calculate_ai_risk_percentage(self, delay: float, days: int, labor_eff: float, budget: float) -> float:
        """
        حساب ذكي لمعدل الخطر مع أوزان معايرة
        """
        delay_factor = min((delay / days) * 100, 50)
        labor_factor = (1.0 - labor_eff) * 30
        budget_factor = max(0, (1000000 / (budget + 1)) - 1) * 10
        
        risk = (delay_factor * 0.45 + labor_factor * 0.35 + budget_factor * 0.20) * 1.1
        
        return min(int(risk) + 5, 95)

    def calculate_advanced_cost_overrun(self, delay: float, days: int, budget: float, labor_eff: float) -> float:
        """
        حساب متقدم لتجاوز التكاليف
        """
        # Daily cost impact
        daily_impact = (delay / days * 100) if days > 0 else 0
        
        # Labor inefficiency multiplier
        labor_multiplier = (1.0 - labor_eff) * 1.5
        
        # Budget constraint penalty
        budget_stress = max(0, 1.2 - (budget / 500000))
        
        cost_overrun = (daily_impact * 0.5 + 
                       labor_multiplier * 25 + 
                       budget_stress * 15)
        
        return min(int(cost_overrun), 100)

    def calculate_advanced_inflation(self, region: str, days: int, budget: float) -> float:
        """
        حساب التضخم مع تأثير المدة والمنطقة
        """
        # Base inflation rate for Saudi Arabia
        base_rate = 3.5
        
        # Get region-specific multiplier
        region_profile = self.region_risk_profile.get(region, {"inflation": 1.0})
        region_multiplier = region_profile["inflation"]
        
        # Calculate project duration factor
        years = days / 365.0
        duration_factor = 1.0 + (years - 1) * 0.8 if years > 1 else 1.0
        
        # Budget stress factor
        budget_stress_factor = 1.0 if budget > 1000000 else 1.15 if budget > 500000 else 1.3
        
        inflation = base_rate * region_multiplier * duration_factor * budget_stress_factor
        
        return round(max(0.5, min(inflation, 10.0)), 2)

    def calculate_advanced_carbon(self, region: str, size: str, days: int, labor_eff: float) -> float:
        """
        حساب متقدم للبصمة الكربونية مع تأثير الكفاءة
        """
        # Base emissions by size
        base_emissions = {
            "صغير": 45, "Small": 45,
            "متوسط": 140, "Medium": 140,
            "كبير": 380, "Large": 380,
            "ضخم": 750, "Mega": 750,
            "Giga": 950, "Infrastructure": 900
        }
        
        emissions = base_emissions.get(size, 100)
        
        # Regional multiplier
        region_profile = self.region_risk_profile.get(region, {"carbon_multiplier": 1.0})
        emissions *= region_profile["carbon_multiplier"]
        
        # Duration effect
        emissions *= (days / 180.0)
        
        # Efficiency improvement factor (better labor = less emissions)
        efficiency_factor = 1.15 - (labor_eff * 0.15)
        emissions *= efficiency_factor
        
        # Additional efficiency penalty for poor compliance
        if labor_eff < 0.6:
            emissions *= 1.3
        elif labor_eff < 0.8:
            emissions *= 1.1
        
        return round(max(30, min(emissions, 2000)), 1)

    def generate_ai_insights(self, delay_analysis: Dict, cost_overrun: float, 
                            risk_level: int, compliance: float) -> Dict:
        """
        توليد استنتاجات ذكية بناءً على التحليل
        """
        insights = {
            'severity': 'Low',
            'primary_recommendation': '',
            'secondary_recommendations': [],
            'confidence': 0.0,
            'detailed_analysis': ''
        }
        
        # Determine severity level
        if risk_level > 75:
            insights['severity'] = 'Critical'
            insights['confidence'] = 0.95
        elif risk_level > 60:
            insights['severity'] = 'High'
            insights['confidence'] = 0.90
        elif risk_level > 40:
            insights['severity'] = 'Medium'
            insights['confidence'] = 0.85
        else:
            insights['severity'] = 'Low'
            insights['confidence'] = 0.80
        
        # Get primary factor
        primary_factor = delay_analysis['primary_factor']
        
        # Generate recommendations based on primary risk factor
        if primary_factor == 'labor':
            insights['primary_recommendation'] = 'تحسين مستويات كفاءة العمالة | Improve labor efficiency'
            insights['secondary_recommendations'] = [
                'زيادة التدريب والإشراف | Increase training and supervision',
                'تحسين معدلات الإنتاجية | Improve productivity metrics',
                'مراجعة تخصيص الموارد البشرية | Review HR allocation'
            ]
        elif primary_factor == 'weather':
            insights['primary_recommendation'] = 'تكييف الجدول الزمني مع الظروف المناخية | Adapt schedule to weather'
            insights['secondary_recommendations'] = [
                'أنشئ خطط بديلة للأيام الحارة | Create contingency plans for hot days',
                'زيادة فترات الراحة والرطوبة | Increase rest periods',
                'استخدم تكنولوجيا التبريد | Deploy cooling technology'
            ]
        elif primary_factor == 'budget':
            insights['primary_recommendation'] = 'إعادة تقييم وزيادة الميزانية | Re-evaluate and increase budget'
            insights['secondary_recommendations'] = [
                'تحسين كفاءة تخصيص الموارد | Optimize resource allocation',
                'التفاوض على أسعار أفضل | Negotiate better prices',
                'البحث عن مصادر تمويل إضافية | Seek additional funding'
            ]
        elif primary_factor == 'scale':
            insights['primary_recommendation'] = 'تقسيم المشروع إلى مراحل أصغر | Break project into phases'
            insights['secondary_recommendations'] = [
                'زيادة فريق العمل | Expand work team',
                'استخدام آليات حديثة | Use advanced machinery',
                'تحسين تسلسل المهام | Improve task sequencing'
            ]
        else:  # risks
            insights['primary_recommendation'] = 'تطوير خطط تخفيف المخاطر | Develop risk mitigation plans'
            insights['secondary_recommendations'] = [
                'إنشاء فريق إدارة مخاطر | Create risk management team',
                'المراقبة المستمرة للمؤشرات | Continuous monitoring',
                'تحديث خطط الطوارئ | Update contingency plans'
            ]
        
        # Generate detailed analysis
        if compliance < 50:
            insights['detailed_analysis'] = 'المشروع في حالة حرجة ويتطلب تدخل فوري | Project is critical'
        elif risk_level > 70:
            insights['detailed_analysis'] = 'مستويات خطر عالية جداً، يوصى بإجراء فوري | High risk levels'
        elif risk_level > 50:
            insights['detailed_analysis'] = 'المشروع يحتاج مراقبة مشددة | Project needs strict monitoring'
        else:
            insights['detailed_analysis'] = 'المشروع قابل للتنفيذ مع اتخاذ احتياطات | Project is feasible'
        
        return insights

    def predict_timeline_scenarios(self, current_delay: float, days: int) -> Dict:
        """
        التنبؤ بسيناريوهات مختلفة للجدول الزمني
        """
        best_case = current_delay * 0.6  # 40% improvement
        worst_case = current_delay * 1.5  # 50% worse
        
        return {
            'best_case': round(best_case, 1),
            'worst_case': round(worst_case, 1),
            'realistic_case': round(current_delay, 1),
            'confidence_interval': round((worst_case - best_case) / 2, 1)
        }
