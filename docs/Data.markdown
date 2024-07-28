---
layout: page
title: Data
permalink: /data/
---

<ul>
  {% for post in site.posts %}
    {% if post.categories contains 'data' %}
      <li>
        <a href="{{ post.url }}">{{ post.title }}</a>
        <small>{{ post.date | date: "%B %d, %Y" }}</small>
      </li>
    {% endif %}
  {% endfor %}
</ul>