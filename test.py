from lxml import html

import math_scraper

math = html.fromstring(
        '<td bgcolor="#cce2f3" nowrap=""><font size="4" color="red"><tt><b>&nbsp;6.708&nbsp;37&nbsp;x&nbsp;10<sup>-39</sup>       (GeV/c<sup>2</sup>)<sup>-2</sup>  </b></tt></font></td>')

print(math_scraper.html_math_parse(math))

