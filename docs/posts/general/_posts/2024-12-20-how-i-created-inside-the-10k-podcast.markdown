---
layout: post
title:  "How I Created a Podcast using NotebookLM"
date:   2024-12-20 00:00:00 -0500
categories: podcast
author: "Jacob Ferraiolo"
toc: true
image: "assets/inside_the_10k/inside_the_10k.webp"
---
![Inside the 10-K](/assets/inside_the_10k/inside_the_10k.webp){: width="500" height="500" }

<h2> Today's post </h2>
* Table of contents
{:toc}

# Summary
[Inside the 10-K](https://open.spotify.com/show/1UaYUVQkBtg2h7aFhx9uVY?si=4df99530381a48a4) 
is an AI generated podcast that relies solely on SEC filings
to analyze company business models, financial performance, and speculate on
investment opportunities.

# Why Did I Create this Podcast?

>Studies reviewed by the Library of Congress
>indicate that U.S. retail investors lack basic financial literacy. The studies demonstrate
>that investors have a weak grasp of elementary financial concepts and lack critical
>knowledge of ways to avoid investment fraud. 

- [Study Regarding Financial Literacy Among Investors](https://www.investor.gov/sites/investorgov/files/2019-02/917-financial-literacy-study-part1.pdf)

When I created *Inside the 10-K*, my goal was to make corporate filings more 
accessible and engaging. These annual company reports are often dense and 
intimidating, but they’re filled with stories about how businesses grow, 
manage risks, and navigate their markets. I wanted to bridge the gap between 
dry financial documents and everyday investors, turning boilerplate text 
into clear, actionable insights.

In this post, I’ll share why I started the show, how I transformed complex 
filings into a digestible format, and what I learned while building a 
production pipeline. I will also share my future plans for this project.

Ultimately, my hope is that anyone—finance professional 
or curious outsider—can find value in these deep dives into corporate strategy.

# The Trouble with Stock Analysis
The main problem equity investors face is not a lack of data -- instead it's the
opposite. There are countless sources of data each claiming to hold novel insights
frequently behind a paywall. 

Investors need to focus on the data that really matters,
but all too frequently, investors end up prioritizing whichever source can
present information in the most stimulating way. Instead of reading annual
reports directly from company's management, investors rely on analyst reports
in the best case and Reddit comments in the worst case.

# Leveraging Annual Reports

Warren Buffett himself stresses the importance of annual reports through [his 
reading habits](https://fs.blog/warren-buffett-information/) and recent studies
have shown a remarkable ability to [forecast financial performance based solely
on LLM's analysis of SEC filings](https://arxiv.org/html/2407.17866v1).

If SEC filings are sufficient to provide investors with an edge, significant
benefit exists in making these reports more accessible to the retail investor.

Recent advancements in AI -- specifically around Large Language Models -- provide
a perfect tool to synthesize large amounts of textual data. Google recently
launched their tool, NotebookLM that allows users to upload source documents
and generate podcast episodes consisting of two hosts discussing the source 
material.

[This tool was designed to help the layperson make sense of complex information.](
https://blog.google/technology/ai/notebooklm-audio-overviews/) The analysis of 
SEC filings seems like the perfect use case for such a tool. Let's take a look
at how we can convert these dense, oftentimes dry, financial filings into a more
accessible format.

# Creating a Podcast

Generating a podcast using NotebookLM is incredibly simple. Simply:

1. **Go to the NotebookLM site**
As of December 2024, [NotebookLM](https://notebooklm.google.com/) is completely 
free. You just need a Google account. Once you log in create a new notebook.
2. **Upload your source documents**
All SEC filings can be found on [SEC.gov](https://www.sec.gov/search-filings) or on
individual company's investor relations pages. You can either download these files
and upload them to NotebookLM or you can link directly to these docs in the NotebookLM interface.
![NotebookLM interface](/assets/inside_the_10k/notebooklm_upload_docs.webp)
3. **Customize the Instructions**
NotebookLM lets you enter a custom prompt that can be used to shape how the podcast
is generated. Here you can specify the intended audience or detail an episode structure.
![Customize Podcast](/assets/inside_the_10k/customize_podcast.webp)
4. **Generate the Podcast**
Now click on "Generate" to create your podcast. 
5. **Edit the audio**
From there I download the audio file and do some minor editing in Garageband like
adding the disclaimer.
6. **Upload to a podcast platform**
Go to [Spotify for Creators](https://creators.spotify.com/pod/dashboard/home) to
create a podcast account and upload your newly created episode.

# Future Vision

- **Automating the pipeline:** There are far too many companies for me to manually create a podcast for each one. I would like to automate this pipeline to automatically retrieve new annual reports, generate the podcast, and upload to Spotify
- **Expanding to industry reports:** I want to upload numerous annual reports for companies in the same industry and see if the podcast can generate an "industry report" 
- **Expand to YouTube:** I intentionally haven't put episodes on Youtube because of the video requirement
- **Diversify content types:** I would like to generate text summaries, sentiment analysis, and a newsletter to accompany the podcast

# Conclusion

*Inside the 10-K* has proven to be a cool way for me to combine my fascination with financial
markets with my interest in new technologies. By utilizing LLMs to efficiently synthesize
and break down financial reports into an easily accessible and digestible format, I get to 
experiment with cutting-edge technology in a domain I am passionate about. 

Additionally, this provides a seemingly needed resource to investors in today's world
of noise. Arguably, the most relevant important information on company performance
and future prospects directly available in an easy to process format.

If you're interested in checking out the podcast, you can find the Tesla episode on 
[Spotify](https://open.spotify.com/episode/10SGBzYXHG4Le4uXcTjOZU?si=ff2ed58b3d0a4cab) 
or [Apple Podcasts](https://podcasts.apple.com/us/podcast/teslas-10-k-accelerating-through-the-numbers/id1781824506?i=1000678239924).



