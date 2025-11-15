InteractionTerm <- function(yourdata,
                            target,
                            interaction1,
                            interaction2) {
  
  # load libraries
  library(dplyr)
  library(ggplot2)
  library(patchwork)
  
  # ensure correct datatypes
  yourdata[[interaction1]] <- as.numeric(yourdata[[interaction1]])
  
  yourdata[[interaction2]] <- as.numeric(yourdata[[interaction2]])
  
  yourdata[[target]] <- as.numeric(yourdata[[target]])
  
  
  # plot for evaluating normality of second term to consider it for discretizing
  plot1 <- ggplot(data = yourdata,
                 aes(x= .data[[interaction2]])) +
    geom_histogram() +
    labs(title = "Interaction 2 Histogram")
  
  # quantiles for splitting low, middle, high
  quants <- quantile(x= yourdata[[interaction2]],
                     probs = c(1/4,
                               3/4))
  
  # creating new DF with discretionized interaction2, IQR = Middle, the rest can be inferred
  withDiscretion <- yourdata %>%
    mutate(
      LVLinteraction2 = case_when(.data[[interaction2]] <= quants[1] ~ "Low",
                                  .data[[interaction2]] >= quants[2] ~ "High",
                                  TRUE ~ "Middle"
                                  )
      )
  
  withDiscretion$LVLinteraction2 <- as.factor(withDiscretion$LVLinteraction2)
  
  # first a plot with the continuous variable as color
  plot2 <- ggplot(data = yourdata,
                  aes(x= .data[[interaction1]],
                      y= .data[[target]],
                      colour= .data[[interaction2]])) +
    geom_smooth(method = "lm") +
    scale_color_gradient(low = "blue",
                         high = "red") +
    geom_point() +
    labs(title = "Continuous")
  
  # now the discretized plot
  plot3 <- ggplot(data = withDiscretion,
                  aes(x= .data[[interaction1]],
                      y= .data[[target]],
                      colour= LVLinteraction2)) +
    geom_smooth(method = "lm") +
    scale_color_discrete() +
    labs(title =  "Discretized")
  
  plot4 <- ggplot(data = yourdata,
                  aes(x= .data[[interaction1]])) +
    geom_histogram() +
    labs(title = "Interaction 1 Histogram")
  
  # create a centered term for the two interaction terms in continuous, but just the continuous of the discretized
  yourdata <- yourdata %>%
    mutate(
      interaction1centered = .data[[interaction1]] - mean(.data[[interaction1]], 
                                                          na.rm = TRUE) ,
      interaction2centered = .data[[interaction2]] - mean(.data[[interaction2]],
                                                          na.rm = TRUE)
    )
  
  # create a centered term in the discretized
  withDiscretion <- withDiscretion %>%
    mutate(
      interaction1centered = .data[[interaction1]] - mean(.data[[interaction1]],
                                                          na.rm = TRUE
                                                          )
      )
  
  # create LM with the interaction continuous
  
  ## create a string of the full formula but use the paste function
  formulaLMconWith <- as.formula(
    paste(
      target, "~ . + interaction1centered * interaction2centered -", interaction1, "-", interaction2 
      )
    )
  
  LMconWith <- lm( formula = formulaLMconWith , 
                   data = yourdata)
  ##results:
  resLMconWith <- summary(LMconWith)
  
  
  # create LM without the interaction term
  
  ## create formula by pasting
  formulaLMconWithOut <- as.formula(
    paste(
      target, "~ . -", interaction1, "-", interaction2
      )
    )
  
  LMconWithOut <- lm(formula = formulaLMconWithOut ,
                      data = yourdata)
  #results:
  resLMconWithOut <- summary(LMconWithOut)
  
  # create dummy LM with the interaction term
  
  ## create the formula
  formulaLMcatWith <- as.formula(
    paste(
      target, "~ . + interaction1centered * LVLinteraction2 -", interaction1, "-", interaction2
      )
    )
  
  LMcatWith <- lm( formula = formulaLMcatWith ,
                   data = withDiscretion)
  #results:
  resLMcatWith <- summary(LMcatWith)
  
  # create dummy LM without the interaction term
  
  ## create formula
  formulaLMcatWithOut <- as.formula(
    paste(
      target, "~ . + interaction1centered + LVLinteraction2 -", interaction1, "-", interaction2 
      )
    )
  
  LMcatWithOut <- lm( formula = formulaLMcatWithOut ,
                      data = withDiscretion)
  #results:
  resLMcatWithOut <- summary(LMcatWithOut)
  
  # now need to patchwork the plots together
  plots <- (plot2 + plot3) / (plot4 + plot1)
  
  
  return(list(
    Variable_plots = plots,
    continuous_interaction_model = LMconWith,
    results_continuous_interaction =resLMconWith,
    continuous_model = LMconWithOut,
    results_continuous = resLMconWithOut,
    categorized_interaction_model = LMcatWith,
    results_discrete_interaction = resLMcatWith,
    categorized_model_without_interaction = LMcatWithOut,
    results_discrete = resLMcatWithOut
  ))
}