"""Test configuration."""

import json
from pathlib import Path
from typing import Any, Type

from dbt_score.models import Model
from dbt_score.rule import Rule, RuleViolation, rule
from pytest import fixture


@fixture
def raw_manifest() -> Any:
    """Mock the raw manifest."""
    return json.loads(
        (Path(__file__).parent / "resources" / "manifest.json").read_text(
            encoding="utf-8"
        )
    )


@fixture
def model1(raw_manifest) -> Model:
    """Model 1."""
    return Model.from_node(raw_manifest["nodes"]["model.package.model1"], [])


@fixture
def model2(raw_manifest) -> Model:
    """Model 2."""
    return Model.from_node(raw_manifest["nodes"]["model.package.model2"], [])


@fixture
def decorator_rule() -> Type[Rule]:
    """An example rule created with the rule decorator."""

    @rule()
    def example_rule(model: Model) -> RuleViolation | None:
        """Description of the rule."""
        if model.name == "model1":
            return RuleViolation(message="Model1 is a violation.")
        return None

    return example_rule


@fixture
def decorator_rule_no_parens() -> Type[Rule]:
    """An example rule created with the rule decorator without parentheses."""

    @rule
    def example_rule(model: Model) -> RuleViolation | None:
        """Description of the rule."""
        if model.name == "model1":
            return RuleViolation(message="Model1 is a violation.")
        return None

    return example_rule


@fixture
def decorator_rule_args() -> Type[Rule]:
    """An example rule created with the rule decorator with arguments."""

    @rule(description="Description of the rule.")
    def example_rule(model: Model) -> RuleViolation | None:
        if model.name == "model1":
            return RuleViolation(message="Model1 is a violation.")
        return None

    return example_rule


@fixture
def class_rule() -> Type[Rule]:
    """An example rule created with a class."""

    class ExampleRule(Rule):
        """Example rule."""

        description = "Description of the rule."

        def evaluate(self, model: Model) -> RuleViolation | None:
            """Evaluate model."""
            if model.name == "model1":
                return RuleViolation(message="Model1 is a violation.")
            return None

    return ExampleRule