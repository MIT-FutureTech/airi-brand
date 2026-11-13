# AIRI brand kit 2.0.0. Generated from tokens.json by dev/build-kit/build.py. Do not edit by hand.
#
# AIRI colours for R figures. One shared file, so every paper uses the same values.
#   source("airi_palette.R")
#   ggplot(d, aes(x, y, fill = is_finding)) + geom_col() +
#     scale_fill_manual(values = c(`TRUE` = airi$color[["primary"]], `FALSE` = airi$color[["gray"]])) +
#     theme_airi()
#   scale_fill_gradientn(colours = airi_ramp("red"))    # more means more risk
#   scale_fill_gradientn(colours = airi_ramp("blue"))   # more is only more
#   scale_fill_manual(values = airi$categorical)         # named categories, never red

airi <- list(
  color = c(primary = "#A32035", primary_hover = "#8A1B2D", primary_dark = "#5E0E20", primary_light = "#D07886", red_500 = "#B8455A", red_300 = "#E29CA8", red_tint = "#F8E1E5", red_wash = "#FBF3F4", blue = "#2171B5", blue_dark = "#084594", blue_tint = "#DCE9F4", highlight = "#FFF0B3", text = "#1A1A1A", text_muted = "#666666", gray = "#898A8D", rule = "#CCCCCC", border = "#D9D9D9", fill = "#F3F3F3", background = "#FAFAFA", surface = "#FFFFFF", white = "#FFFFFF", link = "#A32035", link_hover = "#8A1B2D", link_visited = "#5E0E20", focus = "#A32035", good = "#3A8F5C", good_ink = "#17653C", good_tint = "#E3F1EA", partial = "#E8A317", partial_ink = "#8A5A18", partial_tint = "#FCF3E3", info_ink = "#084594"),
  highlight = c(subject = "#A32035", context = "#898A8D"),
  pair = c("#A32035", "#E29CA8"),
  categorical = c(blue = "#2171B5", sky = "#6BAED6", violet = "#55399E", pink = "#CC6699", orange = "#D4762C", gold = "#D9A531", teal = "#138A73", other = "#898A8D"),
  categorical_ink = c(blue = "#084594", sky = "#084594", violet = "#55399E", pink = "#A3446F", orange = "#A54A0C", gold = "#7F5D00", teal = "#0B6655", other = "#666666"),
  categorical_tint = c(blue = "#E0EBF5", sky = "#EAF4F9", violet = "#E7E3F1", pink = "#F8EAF1", orange = "#F9ECE1", gold = "#FAF2E2", teal = "#DEEFEB", other = "#F3F3F3"),
  severity = c("#E29CA8", "#D07886", "#B8455A", "#A32035", "#5E0E20"),
  severity_none = "#F3F3F3",
  red = c("#FBF3F4", "#E29CA8", "#D07886", "#B8455A", "#A32035", "#5E0E20"),
  blue = c("#EFF6FF", "#C6DBEF", "#9ECAE1", "#6BAED6", "#4292C6", "#2171B5", "#084594"),
  diverging = c("#084594", "#4292C6", "#9ECAE1", "#F3F3F3", "#E29CA8", "#B8455A", "#5E0E20"),
  status = c(good = "#3A8F5C", partial = "#E8A317", poor = "#A32035", none = "#D9D9D9"),
  chrome = c(text = "#1A1A1A", axis_label = "#666666", axis_line = "#CCCCCC", grid = "#D9D9D9", background = "#FFFFFF", uncertainty = "#D9D9D9", no_data = "#F3F3F3"),
  font = "Figtree"
)

# n colours along a named ramp ("red", "blue" or "diverging").
airi_ramp <- function(name = c("red", "blue", "diverging"), n = 256) {
  name <- match.arg(name)
  grDevices::colorRampPalette(unname(airi[[name]]))(n)
}

# ggplot2 theme. Sizes are for print figures at final size.
theme_airi <- function(base_size = 8, base_family = airi$font) {
  ggplot2::theme_minimal(base_size = base_size, base_family = base_family) +
    ggplot2::theme(
      text = ggplot2::element_text(colour = airi$chrome[["text"]]),
      plot.title = ggplot2::element_text(size = 9.5, face = "bold", hjust = 0),
      plot.title.position = "plot",
      axis.text = ggplot2::element_text(colour = airi$chrome[["axis_label"]]),
      axis.title = ggplot2::element_text(colour = airi$chrome[["axis_label"]]),
      axis.line.x = ggplot2::element_line(colour = airi$chrome[["axis_line"]]),
      panel.grid.major = ggplot2::element_line(colour = airi$chrome[["grid"]], linewidth = 0.3),
      panel.grid.major.x = ggplot2::element_blank(),
      panel.grid.minor = ggplot2::element_blank(),
      legend.position = "top",
      legend.justification = "left"
    )
}
