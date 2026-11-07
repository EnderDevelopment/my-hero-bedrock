effect @s strength 8 2 true
effect @s fire_resistance 12 0 true
execute at @s run particle minecraft:large_explosion ~ ~1 ~
execute at @s run playsound random.explode @a ~ ~ ~ 1 1
tp @s ^ ^ ^2
title @s actionbar §cExplosion activated!
