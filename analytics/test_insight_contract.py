#!/usr/bin/env python3

from insight_contract import (
    InsightType, SeverityLevel, ConfidenceLevel, 
    ContributingFactor, Insight, InsightVocabulary, InsightDataStructure
)

def test_insight_vocabulary():
    """Test the insight vocabulary definitions"""
    print("=== Insight Vocabulary Test ===")
    
    # Test getting all insight types
    all_insights = InsightVocabulary.get_all_insight_types()
    print(f"Total insight types defined: {len(all_insights)}")
    
    # Test specific insight definition
    timing_def = InsightVocabulary.get_definition(InsightType.TIMING_INCONSISTENCY)
    print(f"\nTiming Inconsistency Definition:")
    print(f"  Name: {timing_def['name']}")
    print(f"  Definition: {timing_def['definition']}")
    print(f"  Supporting metrics: {timing_def['supporting_metrics']}")
    print(f"  ML sources: {timing_def['ml_sources']}")
    
    # Test insights by ML source
    weakness_insights = InsightVocabulary.get_insights_by_ml_source("weakness_classifier")
    print(f"\nInsights from weakness_classifier: {len(weakness_insights)}")
    for insight in weakness_insights:
        print(f"  - {insight.value}")

def test_insight_creation():
    """Test creating structured insight objects"""
    print("\n=== Insight Creation Test ===")
    
    # Create contributing factors
    factors = [
        ContributingFactor(
            feature_name="anti_air_reaction_test_timing_error_std",
            feature_value=75.2,
            expected_range="10-50ms",
            interpretation="High timing variance indicates inconsistent execution"
        ),
        ContributingFactor(
            feature_name="whiff_punish_test_window_offset_std", 
            feature_value=45.8,
            expected_range="5-30ms",
            interpretation="Inconsistent punish timing"
        )
    ]
    
    # Create insight
    insight = InsightDataStructure.create_insight(
        insight_type=InsightType.TIMING_INCONSISTENCY,
        severity=SeverityLevel.MODERATE,
        confidence=ConfidenceLevel.LIKELY,
        contributing_factors=factors,
        affected_minigames=["anti_air_reaction_test", "whiff_punish_test"],
        supporting_metrics={
            "anti_air_reaction_test_timing_error_std": 75.2,
            "whiff_punish_test_window_offset_std": 45.8
        }
    )
    
    print(f"Created insight:")
    print(f"  ID: {insight.insight_id}")
    print(f"  Type: {insight.insight_type.value}")
    print(f"  Severity: {insight.severity.value}")
    print(f"  Confidence: {insight.confidence.value}")
    print(f"  Explanation: {insight.explanation_text}")
    print(f"  Affected minigames: {insight.affected_minigames}")
    print(f"  Contributing factors: {len(insight.contributing_factors)}")
    
    # Validate insight
    errors = InsightDataStructure.validate_insight(insight)
    if errors:
        print(f"  Validation errors: {errors}")
    else:
        print("  Insight validation passed")

def test_all_insight_types():
    """Test creating insights for all defined types"""
    print("\n=== All Insight Types Test ===")
    
    all_types = InsightVocabulary.get_all_insight_types()
    
    for insight_type in all_types:
        definition = InsightVocabulary.get_definition(insight_type)
        
        # Create minimal insight for testing
        factors = [
            ContributingFactor(
                feature_name="test_metric",
                feature_value=1.0,
                expected_range="0-1",
                interpretation="Test factor"
            )
        ]
        
        insight = InsightDataStructure.create_insight(
            insight_type=insight_type,
            severity=SeverityLevel.LOW,
            confidence=ConfidenceLevel.EMERGING,
            contributing_factors=factors,
            affected_minigames=["test_minigame"],
            supporting_metrics={"test_metric": 1.0}
        )
        
        print(f"{definition['name']}: {insight.explanation_text}")

def test_ml_source_mapping():
    """Test mapping ML sources to insight types"""
    print("\n=== ML Source Mapping Test ===")
    
    ml_sources = ["weakness_classifier", "trend_analyzer", "clustering", "feature_extractor"]
    
    for source in ml_sources:
        insights = InsightVocabulary.get_insights_by_ml_source(source)
        print(f"\n{source} can generate {len(insights)} insight types:")
        for insight in insights:
            definition = InsightVocabulary.get_definition(insight)
            print(f"  - {definition['name']}")

def main():
    test_insight_vocabulary()
    test_insight_creation()
    test_all_insight_types()
    test_ml_source_mapping()
    
    print("\n=== Insight Contract System Ready ===")
    print("Taxonomy defined with 10 insight types")
    print("Vocabulary provides canonical definitions")
    print("Data structure supports structured insight creation")
    print("Validation ensures insight quality")
    print("ML source mapping enables traceability")

if __name__ == "__main__":
    main()