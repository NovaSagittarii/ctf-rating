/** copy teams leaderboard from ctftime */
copy([...document.querySelectorAll('table.table-striped tr')].map(x => x.innerText.replace(/\t+/g, '\t')).join('\n'))

/** process output */
copy(`Maple Mallard Magistrates 3519 24
perfect r00t 3289 53
Sauercloud 3174 102
Poland Can Into Space 3172 10
💦​ 3106 44
isanapap 3088 12
TeamItaly 3016 30
D0G$ 3015 6
DoseGang 3009 4
DiceGang 2996 305
The Parliament of Ducks 2996 5
A*0*E 2993 119
Project Sekai 2965 255
More Smoked Leet Chicken 2941 682
CodeR00t 2916 3
Spatenbräu 2910 8
b1o0p 2908 29
217 2859 397
pasten 2857 201
WreckTheLine 2849 384
Water Paddler 2847 165
StarBugs 2839 28
justCatTheFish 2831 547
0xffa 2829 25
Cykorkinesis 2829 20
kijitora 2826 12`.split('\n').map(x => x.split('').reverse().join('').replace(' ', '\t').replace(' ', '\t').split('').reverse().join('')).join('\n'))