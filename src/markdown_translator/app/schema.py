from typing import Optional

from pydantic import BaseModel, Field


class TranslationSegment(BaseModel):
    original: str = Field(..., description="原文（英語）")
    translation: Optional[str] = Field(None, description="翻訳文（日本語）")


class PaperTranslationOutput(BaseModel):
    title: Optional[str] = Field(None, description="論文のタイトルの原文")
    publication_date: Optional[str] = Field(None, description="論文の発行日")
    authors: Optional[str] = Field(None, description="論文の著者")
    segments: list[TranslationSegment] = Field(..., description="原文と翻訳文のペアのリスト")


class SummarizationSegment(BaseModel):
    segment_title: str = Field(..., description="セグメントで何を伝えたいかを表すタイトル")
    summary: str = Field(None, description="セグメントの要約")


class PaperSummaryOutput(BaseModel):
    title: Optional[str] = Field(None, description="論文のタイトルの原文")
    publication_date: Optional[str] = Field(None, description="論文の発行日")
    authors: Optional[str] = Field(None, description="論文の著者")
    summary: Optional[str] = Field(None, description="論文の要約")
    segments: list[TranslationSegment] = Field(..., description="原文と翻訳文のペアのリスト")
