---
layout: page
title: KU Pharma Student Coding Club
hero_label: Education
description: All levels welcome — from beginner to pro, we all learn together at the University of Copenhagen.
permalink: /codeclub-ku/
---

<style>
  /* ── Scoped retro styles for KU Code Club ───────────────────── */
  .ku-retro {
    max-width: none;
    background-color: #333333;
    color: #a8ff99;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    position: relative;
    overflow: hidden;
    margin: 0 calc(50% - 50vw);
    width: 100vw;
    padding: 0 0 3rem;
  }

  /* Animated starfield background */
  .ku-retro::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
      radial-gradient(2px 2px at 20px 30px, #a8ff99, transparent),
      radial-gradient(2px 2px at 40px 70px, #ffff99, transparent),
      radial-gradient(1px 1px at 90px 40px, #e6ffe6, transparent);
    background-size: 100px 100px, 150px 150px, 200px 200px;
    animation: ku-sparkle 4s ease-in-out infinite;
    z-index: 0;
    pointer-events: none;
  }
  @keyframes ku-sparkle {
    0%, 100% { transform: translate(0, 0); }
    50% { transform: translate(15px, 10px); }
  }

  .ku-retro > * { position: relative; z-index: 1; }

  /* Marquee */
  .ku-marquee-wrap {
    background: #ffff99;
    border: 3px solid #a8ff99;
    overflow: hidden;
    padding: 16px 0;
  }
  .ku-marquee {
    display: inline-block;
    white-space: nowrap;
    color: #333333;
    text-shadow: 3px 3px 0 #a8ff99;
    font-size: 22px;
    font-weight: bold;
    animation: ku-marquee 12s linear infinite;
  }
  @keyframes ku-marquee {
    0%   { transform: translateX(100vw); }
    100% { transform: translateX(-100%); }
  }

  /* DNA banner */
  .ku-dna-banner {
    display: flex;
    overflow: hidden;
    height: 120px;
    align-items: center;
  }
  .ku-dna-banner img { width: 14%; flex-shrink: 0; }

  /* Title block */
  .ku-title-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    padding: 1.5rem 1rem;
    flex-wrap: wrap;
  }
  .ku-title-row img {
    width: 28%;
    min-width: 140px;
    max-width: 240px;
    border: 5px solid #ffff99;
    border-radius: 40%;
    box-shadow: 8px 10px 0 rgba(0,0,0,0.4);
  }
  .ku-title {
    font-size: clamp(1.4rem, 3vw, 2.2rem);
    color: #D6C17C;
    text-shadow: 3px 3px 0 #a8ff99, -3px -3px 0 #e6ffe6;
    border: 8px double #ffff99;
    padding: 1.25rem 1.5rem;
    background-color: #E4D7A1;
    border-radius: 10px;
    text-align: center;
    line-height: 1.4;
  }
  .ku-subtitle {
    font-size: 1.4rem;
    color: #ffff99;
    text-align: center;
    text-shadow: 2px 2px 0 #a8ff99;
    margin: 0.5rem 0 1.5rem;
  }

  /* Sections */
  .ku-section {
    background-color: rgba(95, 125, 97, 0.2);
    border: 5px ridge #ffff99;
    padding: 1.5rem;
    margin: 1.25rem 1.5rem;
    text-align: center;
    background-image: linear-gradient(45deg, transparent 40%, rgba(214,193,124,0.05) 40%, rgba(214,193,124,0.05) 60%, transparent 60%);
    position: relative;
    overflow: hidden;
  }
  .ku-section h2 {
    color: #ffff99;
    text-shadow: 1px 1px 0 #a8ff99, -1px -1px 0 #e6ffe6;
    font-size: 1.6rem;
  }
  .ku-section p, .ku-section li {
    font-size: 1.1rem;
    line-height: 2;
    color: #a8ff99;
    text-shadow: 1px 1px 0 #D6C17C;
  }
  .ku-section ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .ku-section a { color: #D6C17C; text-decoration: none; }
  .ku-section a:hover { color: #a8ff99; text-decoration: underline; }

  /* Floating pandas (absolute within section) */
  .ku-panda {
    position: absolute;
    border-radius: 10%;
    opacity: 0.5;
    animation: ku-float 5s ease-in-out infinite;
    pointer-events: none;
    width: 80px;
  }
  @keyframes ku-float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-16px); }
  }

  /* Rotating event text */
  #ku-rotating-text { display: inline-block; cursor: pointer; }
  #ku-rotating-text.rotating { animation: ku-spin 2s linear infinite; }
  @keyframes ku-spin {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
  }

  /* Map */
  .ku-map-wrap { margin: 1rem auto; display: inline-block; }

  /* Footer bar */
  .ku-footer {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 1.5rem;
    font-size: 0.5rem;
    color: #ffff99;
    opacity: 0.6;
  }
</style>

<div class="ku-retro">

  <div class="ku-marquee-wrap">
    <span class="ku-marquee">🧬 ALL LEVELS WELCOME! FROM BEGINNER TO PRO, WE ALL LEARN TOGETHER! &nbsp;&nbsp;&nbsp;&nbsp; 🧬 ALL LEVELS WELCOME! FROM BEGINNER TO PRO, WE ALL LEARN TOGETHER!</span>
  </div>

  <div class="ku-dna-banner">
    <img src="https://www.cpdse.dk/wp-content/uploads/2026/02/1994-DNA.gif" alt="">
    <img src="https://www.cpdse.dk/wp-content/uploads/2026/02/1994-DNA.gif" alt="">
    <img src="https://www.cpdse.dk/wp-content/uploads/2026/02/1994-DNA.gif" alt="">
    <img src="https://www.cpdse.dk/wp-content/uploads/2026/02/1994-DNA.gif" alt="">
    <img src="https://www.cpdse.dk/wp-content/uploads/2026/02/1994-DNA.gif" alt="">
    <img src="https://www.cpdse.dk/wp-content/uploads/2026/02/1994-DNA.gif" alt="">
    <img src="https://www.cpdse.dk/wp-content/uploads/2026/02/1994-DNA.gif" alt="">
    <img src="https://www.cpdse.dk/wp-content/uploads/2026/02/1994-DNA.gif" alt="">
  </div>

  <div class="ku-title-row">
    <img src="https://www.cpdse.dk/wp-content/uploads/2026/02/rotating-molecule.gif" alt="rotating molecule">
    <h1 class="ku-title">🤖<br>PHARMA STUDENT CODING CLUB<br>🤖</h1>
    <img src="https://www.cpdse.dk/wp-content/uploads/2026/02/agitated-modelule.gif" alt="agitated molecule">
  </div>

  <p class="ku-subtitle">2026 EDITION!!!</p>

  <div class="ku-section">
    <h2>📅 ⏰ UPCOMING EVENT ⏰ 📅</h2>
    <p id="ku-rotating-text">
      2nd SESSION<br>
      23/04/2026 from 16:00 to 18:00<br>
      KU, building 21, CPDSE 1st floor (up the stairs, behind the elevator)
    </p>
    <div class="ku-map-wrap">
      <iframe
        src="https://www.openstreetmap.org/export/embed.html?bbox=12.558223307132723%2C55.702974763821835%2C12.561763823032381%2C55.70428057398417&layer=mapnik&marker=55.703627674357115%2C12.55999356508255"
        width="300" height="200"
        style="border:1px solid #a8ff99;border-radius:6px;display:block;"
        loading="lazy"></iframe>
      <small><a href="https://www.openstreetmap.org/?mlat=55.70363&mlon=12.55999#map=19/55.70363/12.55999&layers=N" target="_blank" rel="noopener" style="color:#D6C17C;">View larger map ↗</a></small>
    </div>
    <img src="https://www.cpdse.dk/wp-content/uploads/2026/02/angry-panda_2.gif" class="ku-panda" style="bottom:10px;left:4%;animation-delay:1.5s;" alt="">
    <img src="https://www.cpdse.dk/wp-content/uploads/2026/02/angry-panda_1.gif" class="ku-panda" style="top:10px;right:8%;animation-delay:1s;" alt="">
  </div>

  <div class="ku-section">
    <h2>Spring 2026 Learning Objective:<br>Become Code Literate</h2>
    <p>1. We know essential programming vocabulary.</p>
    <p>2. We can read, write and understand simple code.</p>
    <p>3. We can identify common errors and know how to solve them.</p>
    <p>4. We know how to investigate in order to decipher complicated code.</p>
    <p>💪 If you want to get there, you're in the right place. 👍</p>
    <img src="https://www.cpdse.dk/wp-content/uploads/2026/02/angry-panda_1.gif" class="ku-panda" style="bottom:8px;right:6%;animation-delay:3.33s;" alt="">
    <img src="https://www.cpdse.dk/wp-content/uploads/2026/02/angry-panda_2.gif" class="ku-panda" style="bottom:8px;left:6%;animation-delay:0.42s;" alt="">
  </div>

  <div class="ku-section">
    <h2 style="color:#D6C17C;">WHAT WE OFFER:</h2>
    <ul>
      <li>☕️ Coffee, cake, and free heating!!</li>
      <li>🧮 Mentoring in Programming and Data Science</li>
      <li>🛠️ Hands-on self-paced practice sessions</li>
      <li>🤝 A community of like-minded people</li>
      <li>🎂 Did I say cake already??</li>
      <li>🎇 And much much more!!! 🎇</li>
    </ul>
  </div>

  <div class="ku-section">
    <h2 style="color:#a8ff99;">EMAIL US AT: <a href="mailto:codingclub@cpdse.dk">codingclub@cpdse.dk</a></h2>
  </div>

  <div class="ku-footer">
    <span>NO COPYRIGHT © 2026 PHARMA STUDENT CODING CLUB. ALL RIGHTS RESERVED. TO BREAK YOUR COMPUTER!</span>
    <span>BEST VIEWED IN 640×480 WITH Bristol Soundcard AT 19200 BAUD</span>
  </div>

</div>

<script>
  document.getElementById('ku-rotating-text').addEventListener('click', function() {
    this.classList.toggle('rotating');
  });
</script>
