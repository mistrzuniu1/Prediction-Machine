from LeagueResultPredictor import LeagueResultPredictor

league=LeagueResultPredictor("D1",5)
league.trainClassifiers()
classifier=league.getLogisticRegressionClassifier()
league.getProbabilitiesForUpcomingMatches(classifier)
