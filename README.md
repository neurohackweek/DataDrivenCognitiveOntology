# A (Data-Driven) Cognitive Neuroscience Ontology

This is a text mining project that uses automatic web scraping of relevant literature given terms of interest from the Cognitive Atlas (Poldrack et al., 2011). It includes a few tools from natural language processing to analyse and visualize the resulting corpus of literature. 

Contributors: Tom Donoghue, Ayala Allon, Basak Kilic, Eric Reavis, Mengya Zhang, Juliet Shafgo, Nicole Roberts, Vassiki Chauhan

https://github.com/neurohackweek/DataDrivenCognitiveOntology

## Background

The Cognitive Atlas was developed in order to facilitate knowledge integration and collaboration in the field of cognitive neuroscience. Specifically, it aimed to provide a foundation that could resolve the ambiguous terminology and clarify the distinction between contructs and tasks within the rapidly expanding corpus of cognitive neuroscience research (Poldrack, 2011).

In the six years since it was launched, the Cognitive Atlas has proven to be a successful respository for defining a wide variety of psychological constructs. This includes 806 concepts, 740 tasks, and 220 disorders. However, its goal to map the relationships between these many conceptual units has been less thoroughly achieved. Only [?] relationships have been described, and of the 1766 total constructs, [?] of them have no defined relationships at all. The most recent user contribution was [?] years ago.

We aim to build on the existing structure of the Cognitive Atlas using a data-driven, rather than crowd-sourced methodology. Specifically, we will extract cooccurrences from the PubMed database in order to link related constructs. The use of crowd-sourcing was important to create a meaningful basic structure that was not available using search terms or keywords alone. However, this approach is limited by the willingness and availability of experts to contribute. Moreover, the literature is constantly changing as new findings are published. Constructs and tasks may be applied to novel questions, leading to a rapid evolution of the underlying cognitive ontology.

The data-driven approach can extract the rapidly evolving conceptual relationships, with less need for continued human commitment. This kind of approach has been successful for characterizing specific subfields of cognitive neuroscience (e.g. Neurosynth, ERP-Scanr).

Beyond simply populating the existing Cognitive Atlas, there may be a wide variety of potential future applications—comparing concepts that may differ between subfields, integrating findings from separate domains of the literature, identifying conceptual relationships before they've even emerged in research, or even suggesting topics & tasks for further empirical exploration. Ultimately, we imagine that this could be a flexible exploratory tool for experts and novices looking to understand the field of cognitive neuroscience.




## Primary Goals:
1. What is the structure of cognitive neuroscience concepts present in the literature accessible through PubMed?
2. How do these relationships compare with the relationships already listed in the Cognitive Atlas? Is our analysis consistent with the explicitly defined connections?
3. Does this conceptual organization line up with our intuitions about these concepts? How can we validate this approach?

## Possible future extensions:
* How have important concepts in Cognitive Neuroscience changed over time (i.e. does restricting the range of years change the associations with a given concept)?
* Do different literatures (e.g. human neuroscience vs. primate research) use terminology differently?
* Can we connect this to ERP-Scanr or Neurosynth (i.e. brain/concept mapping)?
* Could we identify superficially distinct topics from disparate areas that may have underlying similarity?
* More broadly, this could be a tool for others to easily and flexibly explore their own questions (comparing subsets of the literature, etc).
