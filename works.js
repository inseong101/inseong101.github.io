const worksList = document.getElementById('works-list');

fetch('publications.json')
  .then((response) => {
    if (!response.ok) throw new Error('Could not load publications.');
    return response.json();
  })
  .then((publications) => {
    worksList.replaceChildren(...publications.map((publication) => {
      const item = document.createElement('article');
      item.className = 'work-item';

      const title = document.createElement('a');
      title.href = publication.url;
      title.target = '_blank';
      title.rel = 'noopener noreferrer';
      title.textContent = publication.title;

      const meta = document.createElement('span');
      meta.className = 'work-meta';
      meta.textContent = [publication.authors, publication.venue, publication.year]
        .filter(Boolean)
        .join(' · ');

      item.append(title, meta);
      return item;
    }));
  })
  .catch(() => {
    worksList.textContent = 'Publications are temporarily unavailable. Please use the Google Scholar link below.';
  });
