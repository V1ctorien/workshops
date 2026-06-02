import string
import scrapy
from scrapy import Request
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


class MangaBaseSpider(scrapy.Spider):

    name = "Manga"
    start_urls = ['https://myanimelist.net/manga.php']

    def parse(self, response):
        """
        Point d'entrée : détecte la base URL depuis un lien visible dans
        horiznav_nav, puis génère toutes les lettres A→Z + le cas '#'
        (titres commençant par un chiffre) sans se fier aux liens affichés.

        Pourquoi ne pas juste itérer sur les href visibles ?
        → MAL tronque le nav (ex: A, B, C ... Z), on raterait les lettres
          intermédiaires exactement comme pour la pagination numérique.
        """
        xp = "//div[@id='horiznav_nav']//li/a/@href"
        visible_urls = response.xpath(xp).extract()

        # On cherche un lien avec un paramètre 'letter=' pour extraire la base URL
        base_url = None
        for url in visible_urls:
            absolute = response.urljoin(url)
            parsed = urlparse(absolute)
            params = parse_qs(parsed.query)
            if 'letter' in params:
                base_url = parsed  # mémorise scheme, netloc, path — on remplacera letter=
                break

        if base_url is None:
            # Aucun lien lettre trouvé, on ne peut pas générer les URLs
            self.logger.warning("Aucun lien 'letter=' trouvé dans horiznav_nav")
            return

        # Génère une Request pour chaque lettre A→Z
        # + '#' qui représente les titres commençant par un chiffre sur MAL
        for letter in list(string.ascii_uppercase) + ['#']:
            new_query = parse_qs(base_url.query)
            new_query['letter'] = [letter]

            new_url = urlunparse((
                base_url.scheme,
                base_url.netloc,
                base_url.path,
                base_url.params,
                urlencode({k: v[0] for k, v in new_query.items()}),
                base_url.fragment
            ))

            yield Request(
                new_url,
                callback=self.parse_manga_list_page
            )

    def parse_manga_list_page(self, response):
        """
        Parse une page de liste manga. Deux responsabilités :
        1. Extraire les données de chaque ligne du tableau
        2. Détecter et générer toutes les pages de pagination (y compris les trous)
        """

        # --- Extraction des données manga ---
        for tr_sel in response.css('div.js-categories-seasonal tr ~ tr'):
            yield {
                "title":    tr_sel.css('a[id] strong::text').extract_first("").strip(),
                "synopsis": tr_sel.css("div.pt4::text").extract_first(""),
                "type_":    tr_sel.css('td:nth-child(3)::text').extract_first("").strip(),
                "episodes": tr_sel.css('td:nth-child(4)::text').extract_first("").strip(),
                "rating":   tr_sel.css('td:nth-child(5)::text').extract_first("").strip(),
            }

        # --- Détection automatique de la pagination ---
        yield from self._generate_pagination_requests(response)

    def _generate_pagination_requests(self, response):
        """
        Détecte automatiquement le pas (step) et la valeur max du paramètre
        d'offset à partir des liens visibles dans div.spaceit, puis génère
        toutes les URLs intermédiaires manquantes.

        Exemple : si on voit show=0, show=50, show=100 ... show=950,
        on génère range(0, 1000, 50) et on ne rate aucune page.
        """

        # Récupère tous les href de pagination visibles
        pagination_urls = response.xpath(
            "//div[@class='spaceit']//a/@href"
        ).extract()

        if not pagination_urls:
            return  # Pas de pagination sur cette page, on s'arrête

        # Extrait la valeur du paramètre 'show' de chaque URL visible
        offsets = []
        base_url = None  # On va conserver l'URL de base pour reconstruire les autres

        for url in pagination_urls:
            absolute_url = response.urljoin(url)
            parsed = urlparse(absolute_url)
            params = parse_qs(parsed.query)

            if 'show' in params:
                try:
                    offset = int(params['show'][0])
                    offsets.append(offset)

                    # On mémorise l'URL de base (sans le paramètre show)
                    # à partir du premier lien valide trouvé
                    if base_url is None:
                        base_url = parsed
                except ValueError:
                    continue  # Ignore les valeurs non numériques

        # S'il n'y a pas assez d'offsets pour calculer un pas, on ne peut rien faire
        if len(offsets) < 2 or base_url is None:
            return

        offsets_sorted = sorted(set(offsets))  # Dédoublonne et trie

        # Détection automatique du pas entre deux pages consécutives
        step = offsets_sorted[1] - offsets_sorted[0]

        # Valeur maximale visible (ex: la page "20" dans "1,2,3...20")
        max_offset = offsets_sorted[-1]

        # Récupère l'offset actuel de la page qu'on est en train de parser
        current_params = parse_qs(urlparse(response.url).query)
        current_offset = int(current_params.get('show', [0])[0])

        # Génère toutes les pages de current_offset+step jusqu'à max_offset inclus
        # → on évite de re-scraper la page courante et les précédentes
        for offset in range(current_offset + step, max_offset + step, step):

            # Reconstruit l'URL complète avec le nouvel offset
            new_query = parse_qs(base_url.query)
            new_query['show'] = [str(offset)]

            new_url = urlunparse((
                base_url.scheme,
                base_url.netloc,
                base_url.path,
                base_url.params,
                urlencode({k: v[0] for k, v in new_query.items()}),
                base_url.fragment
            ))

            yield Request(new_url, callback=self.parse_manga_list_page)
