SHOPS := ShopRed ShopGreen ShopGold ShopSilver ShopDiamond ShopPearl ShopBlack ShopWhite ShopScarlet ShopViolet RouletteRuby RouletteSapphire
%.4bpp: %.png ; ../tools/gbagfx/gbagfx $< $@ -mwidth 2 -mheight 2 -oam
%.gbapal: %.png ; ../tools/gbagfx/gbagfx $< $@

PICS = $(addsuffix .4bpp, $(SHOPS))
PALS = $(addsuffix .gbapal, $(SHOPS))

all: $(PICS) $(PALS)
	