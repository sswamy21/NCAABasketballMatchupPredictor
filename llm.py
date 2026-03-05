from ollama import chat
from ollama import ChatResponse

def format_matchup_for_llm_detailed(summary):
    """
    Comprehensive format - includes all available statistics.
    Organized hierarchically to prevent LLM confusion.
    ~300-400 tokens but information-rich.
    
    Args:
        summary: dict from build_detailed_matchup()
        
    Returns:
        str: Detailed formatted analysis for LLM
    """
    t1 = summary['team1_name']
    t2 = summary['team2_name']
    
    # Determine favorite
    pred_margin = summary.get('PredictedMargin', 0)
    win_prob = summary.get('WinProbability', 0.5)
    
    if pred_margin > 0:
        favorite = t1
        underdog = t2
        fav_prob = win_prob
    else:
        favorite = t2
        underdog = t1
        fav_prob = 1 - win_prob
        pred_margin = -pred_margin
    
    # Market data
    market_spread = summary.get('MarketSpread')
    model_edge = summary.get('ModelEdge')
    
    # Build comprehensive formatted string
    formatted = f"""╔══════════════════════════════════════════════════════════════╗
    ║ MATCHUP ANALYSIS: {t1} @ {t2}
    ╚══════════════════════════════════════════════════════════════╝

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    PREDICTION & MARKET
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Model Prediction:  {favorite} -{pred_margin:.1f}
    Win Probability:   {fav_prob:.1%} ({favorite})
    Market Spread:     {f"{market_spread:+.1f}" if market_spread is not None else 'N/A'}
    Model Edge:        {f"{model_edge:+.1f}" if model_edge is not None else 'N/A'} points
    Cover Margin:      {summary.get('CoverMargin', 'N/A')}

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    TEAM RATINGS (positive = {t1} advantage)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Elo Rating:        {summary.get('Elo_Diff', 0):+6.1f}
    Net Rating:        {summary.get('NetRating_Diff', 0):+6.1f}
    └─ {t1}: {summary.get('NetRating_Team1', 0):6.1f}
    └─ {t2}: {summary.get('NetRating_Team2', 0):6.1f}

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    OFFENSIVE & DEFENSIVE EFFICIENCY
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Offensive Eff:     {summary.get('OffEff_Diff', 0):+6.1f}
    Defensive Eff:     {summary.get('DefEff_Diff', 0):+6.1f}
    Average Off Eff:   {summary.get('Avg_OffEff', 0):6.1f}
    Average Def Eff:   {summary.get('Avg_DefEff', 0):6.1f}

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    FOUR FACTORS (positive = {t1} advantage)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Effective FG%:     {summary.get('eFG_Diff', 0):+6.3f}
    Turnover Rate:     {summary.get('TORate_Diff', 0):+6.3f}
    Off Reb %:         {summary.get('ORebPct_Diff', 0):+6.3f}
    Free Throw Rate:   {summary.get('FTRate_Diff', 0):+6.3f}

    Opponent Four Factors:
    Opp eFG%:          {summary.get('Opp_eFG_Diff', 0):+6.3f}
    Opp TO Rate:       {summary.get('Opp_TORate_Diff', 0):+6.3f}
    Def Reb %:         {summary.get('DRebPct_Diff', 0):+6.3f}
    Opp FT Rate:       {summary.get('Opp_FTRate_Diff', 0):+6.3f}

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    PLAYER QUALITY METRICS (positive = {t1} advantage)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Starting 5 PER:    {summary.get('StarterAvgPER_Diff', 0):+6.1f}
    └─ {t1}: {summary.get('StarterAvgPER_Team1', 0):6.1f}
    └─ {t2}: {summary.get('StarterAvgPER_Team2', 0):6.1f}

    Star Power Index:  {summary.get('StarPowerDiff_Diff', 0):+6.1f}
    └─ {t1}: {summary.get('StarPowerDiff_Team1', 0):6.1f}
    └─ {t2}: {summary.get('StarPowerDiff_Team2', 0):6.1f}

    Bench Production:  {summary.get('BenchPtsPct_Diff', 0):+6.3f}
    └─ {t1}: {summary.get('BenchPtsPct_Team1', 0):6.1%}
    └─ {t2}: {summary.get('BenchPtsPct_Team2', 0):6.1%}

    Bench Depth:       {summary.get('BenchDepth10_Diff', 0):+6.1f} players
    └─ {t1}: {summary.get('BenchDepth10_Team1', 0):6.1f}
    └─ {t2}: {summary.get('BenchDepth10_Team2', 0):6.1f}

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    PACE & STYLE
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Tempo Differential: {summary.get('Tempo_Diff', 0):+6.1f}
    Average Tempo:     {summary.get('Avg_Tempo', 0):6.1f} poss/game
    Tempo Ratio:       {summary.get('Tempo_Ratio', 1):6.3f} ({t1}/{t2})

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    CONSISTENCY & FORM
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Consistency:       {summary.get('Consistency_Diff', 0):+6.1f}
    └─ {t1}: {summary.get('Consistency_Team1', 0):6.1f} (lower = more consistent)
    └─ {t2}: {summary.get('Consistency_Team2', 0):6.1f}

    Form Rating:       {summary.get('FormRating_Diff', 0):+6.1f}
    └─ {t1}: {summary.get('FormRating_Team1', 0):6.1f}
    └─ {t2}: {summary.get('FormRating_Team2', 0):6.1f}

    Opp Strength Adj:  {summary.get('OppStrengthAdj_Diff', 0):+6.1f}

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ADVANCED METRICS
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Win %:             {summary.get('WinPct_Diff', 0):+6.3f}
    Avg Margin:        {summary.get('AvgMargin_Diff', 0):+6.1f}
    Avg Score:         {summary.get('AvgScore_Diff', 0):+6.1f}
    Avg Opp Score:     {summary.get('AvgOppScore_Diff', 0):+6.1f}

    Home Advantage:    {'+' if summary.get('HomeAdvantage', 0) > 0 else ''}{summary.get('HomeAdvantage', 0)} ({t1} is home)
    """
    return formatted


def get_prompt():
    prompt = f""" Role: Lead Sports Data Scientist and Professional Handicapper.
                Context: Analyzing NCAA Basketball matchup data to identify betting value.
                Constraint: Max 800 characters. Technical, objective tone. No fluff.

                Instructions:
                1. Matchup & Market: Start with [Away] @ [Home]. State Win Probability vs. Implied Market Odds.
                2. Efficiency Deep-Dive: Identify the delta in Elo and AdjO/AdjD. Highlight if the gap is driven by a specific unit (e.g., "Home Offense vs. Away Defense").
                3. Tactical Edge: Explain the mismatch intuition. Contrast shooting volume (FGA/3PA) against efficiency (eFG%/TS%). 
                4. Variance & Risk: Identify the "Chaos Factor." Use Foul Rate to predict bench dependency or 3PT% to assess floor/ceiling volatility.
                5. Verdict: State the "Model Edge" (Model Spread minus Market Spread). 

                Format: Use Bold Headers and Bulleted Technical Insights."""
    return prompt

def get_response(summary):
    if isinstance(summary, dict):
        matchup_stats = format_matchup_for_llm_detailed(summary)
    else:
        matchup_stats = str(summary)
    user_msg = (
        "Use the stats below to give 4-6 interpretive insights (edges, risks, matchup drivers). "
        "Do not restate raw numbers; infer causes. If a metric is missing, skip it."
    )

    try:
        response: ChatResponse = chat(
            model="llama3:latest",
            messages=[
                {"role": "system", "content": get_prompt()},
                {"role": "user", "content": user_msg + "\n\n" + matchup_stats}
            ],
            options = {
                "temperature": 0.7,
                "top_p": 0.92,
                "top_k": 60,
                "repeat_penalty": 1.08,
                "mirostat": 2,
                "mirostat_tau": 6.0,
                "mirostat_eta": 0.1,
                "num_ctx": 4096,
                "num_predict": 600
            }
        )
        return response.message.content
    except Exception as e:
        print(f"Error during LLM response generation: {e}")
        return "LLM response generation failed."

summary = {
            'team1_name': 'Team A',
            'team2_name': 'Team B',
            'PredictedMargin': 5.0,
            'WinProbability': 0.6,
            'MarketSpread': -3.0,
            'ModelEdge': 2.0,
            'CoverMargin': 'N/A',
            'Elo_Diff': 10.0,
            'NetRating_Diff': 2.0,
            'NetRating_Team1': 15.0,
            'NetRating_Team2': 13.0,
            'OffEff_Diff': 1.5,
            'DefEff_Diff': -0.5,
            'Avg_OffEff': 110.0,
            'Avg_DefEff': 105.0,
            'eFG_Diff': 0.02,
            'TORate_Diff': -0.01,
            'ORebPct_Diff': 0.03,
            'FTRate_Diff': 0.005,
            'Opp_eFG_Diff': -0.015,
            'Opp_TORate_Diff': 0.02,
            'DRebPct_Diff': -0.025,
            'Opp_FTRate_Diff': 0.01,
            'StarterAvgPER_Diff': 1.2,
            'StarterAvgPER_Team1': 18.5,
            'StarterAvgPER_Team2': 17.3,
            'StarPowerDiff_Diff': 0.8,
            'StarPowerDiff_Team1': 12.0,
            'StarPowerDiff_Team2': 11.2,
            'BenchPtsPct_Diff': 0.05,
            'BenchPtsPct_Team1': 0.25,
            'BenchPtsPct_Team2': 0.20,
            'BenchDepth10_Diff': 2.0,
            'BenchDepth10_Team1': 8.0,
            'BenchDepth10_Team2': 6.0,
            'Tempo_Diff': 1.5,
            'Avg_Tempo': 70.0,
            'Tempo_Ratio': 1.02,
            'Consistency_Diff': -0.3,
            'Consistency_Team1': 5.0,
            'Consistency_Team2': 5.3,
            'FormRating_Diff': 1.0,
            'FormRating_Team1': 8.0,
            'FormRating_Team2': 7.0,
            'OppStrengthAdj_Diff': 0.5,
            'WinPct_Diff': 0.1,
            'AvgMargin_Diff': 2.0,
            'AvgScore_Diff': 5.0,
            'AvgOppScore_Diff': -1.0,
            'HomeAdvantage': 3.0
    }

# print(get_response(summary))
