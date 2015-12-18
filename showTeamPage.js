function showTeamPage(pId, yr, sport, div, org){
      document.results.action = '/stats/StatsSrv/careerteam';
      document.results.doWhat.value = 'display';
      document.results.playerId.value = pId; 
      document.results.coachId.value = pId; 
      document.results.academicYear.value = yr; 
      document.results.sportCode.value = sport; 
      document.results.division.value = div; 
      document.results.orgId.value = org; 
      document.results.submit();
   }