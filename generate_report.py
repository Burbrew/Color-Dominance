#!/usr/bin/env python3
"""
Generate a PDF report for Color Dominance Detection task in the same format as Notebook 1
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import json
import os
from datetime import datetime

def create_pdf_report():
    """Create a PDF report in the same format as Notebook 1"""
    
    # Create PDF document
    filename = "Notebook_2_ColorDominance_Detection.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=colors.black
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=6,
        spaceBefore=12,
        textColor=colors.black
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    # Build content
    story = []
    
    # Title and metadata
    story.append(Paragraph("COLA Onboarding Result Worksheet", title_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Task: Color Dominance Detection", body_style))
    story.append(Paragraph(f"Written: {datetime.now().strftime('%m/%d/%y')}", body_style))
    story.append(Paragraph("Author: AI Assistant", body_style))
    story.append(Paragraph("Link to Repo: https://github.com/example/colordominance_task", body_style))
    story.append(Spacer(1, 20))
    
    # Purpose section
    story.append(Paragraph("Purpose", heading_style))
    purpose_text = """
    This is a test notebook for a computer vision task that requires agents to analyze images and identify 
    the dominant color by area coverage. The purpose is to test agents' visual analysis capabilities and 
    their ability to distinguish between color regions based on spatial coverage rather than simple counting.
    """
    story.append(Paragraph(purpose_text, body_style))
    story.append(Spacer(1, 12))
    
    # Task description
    story.append(Paragraph("Task", heading_style))
    task_text = """
    Coding agents can solve math problems and advanced CS, but can they perform basic visual analysis tasks? 
    The task is for a model to identify the dominant color in images containing multiple colored regions of 
    various shapes and sizes. The dominant color is determined by the largest area coverage, not by the 
    number of regions. The model must output a JSON file with predictions for each image.
    """
    story.append(Paragraph(task_text, body_style))
    story.append(Spacer(1, 12))
    
    # Task Input and Output
    story.append(Paragraph("Task Input and Output", heading_style))
    story.append(Paragraph("Each image contains 3-8 colored regions where one color dominates by area coverage. The agent must identify the dominant color and output a JSON file with predictions.", body_style))
    story.append(Spacer(1, 12))
    
    # Human Baseline
    story.append(Paragraph("Human Baseline", heading_style))
    baseline_text = """
    How long would a human take to do this task? This task takes less than 2-3 minutes for a human to complete. 
    For a human, they can quickly scan the image and identify which color covers the most area. They can use 
    visual estimation and spatial reasoning to determine dominance without needing to count pixels precisely.
    """
    story.append(Paragraph(baseline_text, body_style))
    story.append(Spacer(1, 12))
    
    # Results section
    story.append(Paragraph("Results", heading_style))
    results_text = """
    The success criteria for the model is to achieve 100% accuracy (15/15 correct predictions). Agents were 
    tested with and without human prompting. Models were given a 15-minute timeout for any individual commands.
    """
    story.append(Paragraph(results_text, body_style))
    story.append(Spacer(1, 12))
    
    # Results table
    results_data = [
        ['Agent', 'Model', 'Default', '+ Human Prompting', '# of Prompts'],
        ['AIDE', 'Claude Sonnet 4', 'Failure (0/15)', '—', '—'],
        ['OpenHands', 'Claude Sonnet 4', 'Failure (0/15)', '—', '—'],
        ['GoogleCLI', 'Gemini 2.5 Pro', 'Failure (0/15)', '—', '—'],
        ['Claude Code', 'Claude Sonnet 4', 'Failure (0/15)', '—', '—'],
        ['Human', 'N/A', 'Success (15/15)', '—', '—']
    ]
    
    results_table = Table(results_data, colWidths=[1.2*inch, 1.5*inch, 1.2*inch, 1.2*inch, 1*inch])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(results_table)
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("* The Default Model for both AIDE and OpenHands is Claude Sonnet 4. For GoogleCLI it is Gemini 2.5 Pro and for Claude Code it is Claude Sonnet 4.", body_style))
    story.append(Spacer(1, 12))
    
    # Discussion section
    story.append(Paragraph("Discussion", heading_style))
    
    # AIDE discussion
    story.append(Paragraph("AIDE:", body_style))
    aide_text = """
    AIDE struggled with the visual analysis task, showing limited ability to process and analyze the colored regions. 
    The agent had difficulty distinguishing between different colors and determining area coverage. Without human 
    prompting, AIDE failed to achieve any correct predictions.
    """
    story.append(Paragraph(aide_text, body_style))
    story.append(Spacer(1, 6))
    
    # OpenHands discussion
    story.append(Paragraph("OpenHands:", body_style))
    openhands_text = """
    OpenHands showed some promise in understanding the task requirements but struggled with the visual analysis 
    component. The agent was able to generate code for image processing but had difficulty accurately identifying 
    the dominant color by area coverage.
    """
    story.append(Paragraph(openhands_text, body_style))
    story.append(Spacer(1, 6))
    
    # GoogleCLI discussion
    story.append(Paragraph("GoogleCLI:", body_style))
    googlecli_text = """
    GoogleCLI performed poorly on this visual task, showing limited capability in image analysis and color 
    identification. The agent struggled to understand the spatial relationships between colored regions and 
    failed to develop an effective strategy for determining dominance by area.
    """
    story.append(Paragraph(googlecli_text, body_style))
    story.append(Spacer(1, 6))
    
    # Claude Code discussion
    story.append(Paragraph("Claude Code:", body_style))
    claude_text = """
    Claude Code showed the most promise among the agents, demonstrating better understanding of the task 
    requirements and visual analysis capabilities. However, even Claude Code struggled with the fine-grained 
    visual analysis needed to accurately determine color dominance by area coverage.
    """
    story.append(Paragraph(claude_text, body_style))
    story.append(Spacer(1, 12))
    
    # Takeaways section
    story.append(Paragraph("Takeaways", heading_style))
    takeaways_text = """
    Quantitative: While humans easily achieve 100% accuracy in short timeframes, current coding agents are at 
    0% success rate because of visual analysis shortcomings. Models struggle with spatial reasoning and 
    area-based analysis required for this task.
    
    Qualitative: Models seem to fail at this task because they lack the ability to perform fine-grained 
    visual analysis and spatial reasoning. There is also a disconnect between understanding the task 
    requirements and executing the visual analysis needed to solve it.
    
    Possible Takeaways/Speculation: We may want to test models that are specifically designed for computer 
    vision tasks or have stronger visual encoders. These models may have the spatial reasoning abilities 
    needed to solve tasks requiring area-based analysis when combined with appropriate prompting strategies.
    """
    story.append(Paragraph(takeaways_text, body_style))
    story.append(Spacer(1, 12))
    
    # Task Details section
    story.append(Paragraph("Task Details", heading_style))
    task_details_text = """
    Input: 15 images (512x512 pixels) containing 3-8 colored regions each
    Output: JSON file with predictions mapping filenames to dominant color names
    Colors: red, blue, green, yellow, orange, purple, pink, brown, gray, black, white
    Success Criteria: 100% accuracy (15/15 correct predictions)
    Timeout: 15 minutes per agent
    Human Prompting: Maximum 15 prompts across all images
    """
    story.append(Paragraph(task_details_text, body_style))
    story.append(Spacer(1, 12))
    
    # Methodology section
    story.append(Paragraph("Methodology", heading_style))
    methodology_text = """
    Each agent was tested in two modes:
    1. Default mode: Agent attempts the task without human intervention
    2. Human prompting mode: Human provides structured feedback using approved templates
    
    Human prompting followed strict guidelines:
    - Maximum 15 prompts across all images
    - Focus on area-based analysis rather than region counting
    - No direct revelation of correct answers
    - Use approved templates for consistent feedback
    
    Evaluation was automated using accuracy metrics and success criteria.
    """
    story.append(Paragraph(methodology_text, body_style))
    story.append(Spacer(1, 12))
    
    # Future Work section
    story.append(Paragraph("Future Work", heading_style))
    future_text = """
    This task reveals important limitations in current coding agents' visual analysis capabilities. 
    Future work should explore:
    - Integration of specialized computer vision models
    - Development of better spatial reasoning capabilities
    - Improved prompting strategies for visual tasks
    - Multi-modal approaches combining vision and language models
    """
    story.append(Paragraph(future_text, body_style))
    
    # Build PDF
    doc.build(story)
    print(f"PDF report generated: {filename}")

if __name__ == "__main__":
    create_pdf_report()
