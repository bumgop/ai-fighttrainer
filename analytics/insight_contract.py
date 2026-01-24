from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class InsightType(Enum):
    TIMING_INCONSISTENCY = "timing_inconsistency"
    LATE_REACTIONS = "late_reactions"
    POOR_MIXUP_DEFENSE = "poor_mixup_defense"
    HIGH_VARIANCE_DECISIONS = "high_variance_decisions"
    IMPATIENT_INPUTS = "impatient_inputs"
    MISSED_OPPORTUNITIES = "missed_opportunities"
    DEFENSIVE_WEAKNESS = "defensive_weakness"
    IMPROVING_PERFORMANCE = "improving_performance"
    STABLE_PERFORMANCE = "stable_performance"
    REGRESSING_PERFORMANCE = "regressing_performance"

class SeverityLevel(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"

class ConfidenceLevel(Enum):
    EMERGING = "emerging"      # 0.3-0.5 confidence
    LIKELY = "likely"          # 0.5-0.7 confidence  
    ESTABLISHED = "established" # 0.7+ confidence

@dataclass
class ContributingFactor:
    feature_name: str
    feature_value: float
    expected_range: str
    interpretation: str

@dataclass
class Insight:
    insight_id: str
    insight_type: InsightType
    severity: SeverityLevel
    confidence: ConfidenceLevel
    contributing_factors: List[ContributingFactor]
    explanation_text: str
    affected_minigames: List[str]
    supporting_metrics: Dict[str, float]

class InsightVocabulary:
    """Canonical definitions for all insight types"""
    
    DEFINITIONS = {
        InsightType.TIMING_INCONSISTENCY: {
            "name": "Timing Inconsistency",
            "definition": "Player shows high variance in timing across attempts, indicating unreliable execution",
            "behavior_causes": [
                "Inconsistent reaction speed",
                "Variable input timing",
                "Lack of muscle memory development"
            ],
            "supporting_metrics": [
                "anti_air_reaction_test_timing_error_std",
                "whiff_punish_test_window_offset_std"
            ],
            "ml_sources": ["weakness_classifier", "trend_analyzer"]
        },
        
        InsightType.LATE_REACTIONS: {
            "name": "Late Reactions",
            "definition": "Player frequently responds too slowly to threats and opportunities",
            "behavior_causes": [
                "Slow threat recognition",
                "Delayed decision making",
                "Poor anticipation skills"
            ],
            "supporting_metrics": [
                "anti_air_reaction_test_late_rate",
                "whiff_punish_test_late_rate",
                "whiff_punish_test_miss_rate"
            ],
            "ml_sources": ["weakness_classifier", "feature_extractor"]
        },
        
        InsightType.POOR_MIXUP_DEFENSE: {
            "name": "Poor Mixup Defense",
            "definition": "Player tends to autopilot confirm hits without proper hit confirmation",
            "behavior_causes": [
                "Autopilot gameplay patterns",
                "Poor hit/block recognition",
                "Overcommitment to offense"
            ],
            "supporting_metrics": [
                "hit_confirm_test_false_confirm_rate",
                "hit_confirm_test_decision_error_rate"
            ],
            "ml_sources": ["weakness_classifier"]
        },
        
        InsightType.HIGH_VARIANCE_DECISIONS: {
            "name": "High Variance Decisions", 
            "definition": "Player shows inconsistent decision-making patterns across similar situations",
            "behavior_causes": [
                "Inconsistent game plan execution",
                "Emotional decision making",
                "Lack of systematic approach"
            ],
            "supporting_metrics": [
                "defense_under_pressure_test_block_accuracy_std"
            ],
            "ml_sources": ["clustering", "feature_extractor"]
        },
        
        InsightType.IMPATIENT_INPUTS: {
            "name": "Impatient Inputs",
            "definition": "Player frequently inputs commands too early, showing impatience or poor timing discipline",
            "behavior_causes": [
                "Anticipation over reaction",
                "Anxiety-driven inputs",
                "Poor frame data knowledge"
            ],
            "supporting_metrics": [
                "anti_air_reaction_test_early_rate",
                "whiff_punish_test_early_rate"
            ],
            "ml_sources": ["weakness_classifier"]
        },
        
        InsightType.MISSED_OPPORTUNITIES: {
            "name": "Missed Opportunities",
            "definition": "Player fails to capitalize on advantageous situations",
            "behavior_causes": [
                "Poor opportunity recognition",
                "Hesitation in execution",
                "Conservative play style"
            ],
            "supporting_metrics": [
                "hit_confirm_test_missed_confirm_rate",
                "whiff_punish_test_miss_rate"
            ],
            "ml_sources": ["weakness_classifier", "feature_extractor"]
        },
        
        InsightType.DEFENSIVE_WEAKNESS: {
            "name": "Defensive Weakness",
            "definition": "Player struggles with defensive fundamentals under pressure",
            "behavior_causes": [
                "Poor blocking discipline",
                "Panic under pressure",
                "Inadequate defensive options knowledge"
            ],
            "supporting_metrics": [
                "defense_under_pressure_test_block_accuracy_mean",
                "defense_under_pressure_test_block_accuracy_std"
            ],
            "ml_sources": ["feature_extractor", "weakness_classifier"]
        },
        
        InsightType.IMPROVING_PERFORMANCE: {
            "name": "Improving Performance",
            "definition": "Player shows measurable improvement in key metrics over time",
            "behavior_causes": [
                "Effective practice habits",
                "Skill development progression",
                "Learning from mistakes"
            ],
            "supporting_metrics": ["trend_classification_improving_count"],
            "ml_sources": ["trend_analyzer"]
        },
        
        InsightType.STABLE_PERFORMANCE: {
            "name": "Stable Performance", 
            "definition": "Player maintains consistent performance levels across sessions",
            "behavior_causes": [
                "Established skill plateau",
                "Consistent execution patterns",
                "Reliable fundamentals"
            ],
            "supporting_metrics": ["trend_classification_flat_count"],
            "ml_sources": ["trend_analyzer"]
        },
        
        InsightType.REGRESSING_PERFORMANCE: {
            "name": "Regressing Performance",
            "definition": "Player shows declining performance in key areas over recent sessions",
            "behavior_causes": [
                "Developing bad habits",
                "Inconsistent practice",
                "Overconfidence leading to sloppiness"
            ],
            "supporting_metrics": ["trend_classification_regressing_count"],
            "ml_sources": ["trend_analyzer"]
        }
    }
    
    @classmethod
    def get_definition(cls, insight_type: InsightType) -> Dict:
        """Get canonical definition for an insight type"""
        return cls.DEFINITIONS.get(insight_type, {})
    
    @classmethod
    def get_all_insight_types(cls) -> List[InsightType]:
        """Get all available insight types"""
        return list(cls.DEFINITIONS.keys())
    
    @classmethod
    def get_insights_by_ml_source(cls, ml_source: str) -> List[InsightType]:
        """Get insight types that can be generated from a specific ML source"""
        insights = []
        for insight_type, definition in cls.DEFINITIONS.items():
            if ml_source in definition.get("ml_sources", []):
                insights.append(insight_type)
        return insights

class InsightDataStructure:
    """Utilities for creating and validating insight objects"""
    
    @staticmethod
    def create_insight(
        insight_type: InsightType,
        severity: SeverityLevel,
        confidence: ConfidenceLevel,
        contributing_factors: List[ContributingFactor],
        affected_minigames: List[str],
        supporting_metrics: Dict[str, float]
    ) -> Insight:
        """Create a structured insight object"""
        
        definition = InsightVocabulary.get_definition(insight_type)
        explanation_text = InsightDataStructure._generate_explanation(
            insight_type, severity, confidence, definition
        )
        
        insight_id = f"{insight_type.value}_{severity.value}_{len(affected_minigames)}"
        
        return Insight(
            insight_id=insight_id,
            insight_type=insight_type,
            severity=severity,
            confidence=confidence,
            contributing_factors=contributing_factors,
            explanation_text=explanation_text,
            affected_minigames=affected_minigames,
            supporting_metrics=supporting_metrics
        )
    
    @staticmethod
    def _generate_explanation(
        insight_type: InsightType,
        severity: SeverityLevel, 
        confidence: ConfidenceLevel,
        definition: Dict
    ) -> str:
        """Generate explanation text for an insight"""
        
        name = definition.get("name", insight_type.value)
        base_definition = definition.get("definition", "")
        
        confidence_text = {
            ConfidenceLevel.EMERGING: "shows early signs of",
            ConfidenceLevel.LIKELY: "demonstrates",
            ConfidenceLevel.ESTABLISHED: "consistently exhibits"
        }
        
        severity_text = {
            SeverityLevel.LOW: "minor",
            SeverityLevel.MODERATE: "noticeable", 
            SeverityLevel.HIGH: "significant"
        }
        
        return f"Player {confidence_text[confidence]} {severity_text[severity]} {name.lower()}. {base_definition}"
    
    @staticmethod
    def validate_insight(insight: Insight) -> List[str]:
        """Validate insight object and return any errors"""
        errors = []
        
        if not insight.insight_id:
            errors.append("Missing insight_id")
            
        if not insight.explanation_text:
            errors.append("Missing explanation_text")
            
        if not insight.affected_minigames:
            errors.append("No affected minigames specified")
            
        if not insight.contributing_factors:
            errors.append("No contributing factors provided")
            
        # Validate that insight type has supporting metrics
        definition = InsightVocabulary.get_definition(insight.insight_type)
        expected_metrics = definition.get("supporting_metrics", [])
        
        if expected_metrics:
            found_metrics = [m for m in expected_metrics if m in insight.supporting_metrics]
            if not found_metrics:
                errors.append(f"No supporting metrics found for {insight.insight_type.value}")
        
        return errors