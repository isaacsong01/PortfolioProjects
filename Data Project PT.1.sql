-- SELECT *
-- FROM coviddeaths
-- WHERE continent is not null or continent != ' '
-- ORDER BY 3, 4;


-- SELECT * 
-- FROM covidvaccinations
-- ORDER BY 3,4;

-- Total Deaths vs Population --------------------------------------------------------------
-- Shows what percentage of population died resulting from COVID ---------------------------

-- SELECT location, date, population, total_deaths, (total_deaths/population)*100 as DeathPercentage
-- FROM coviddeaths
-- WHERE location like '%states%'
-- ORDER BY 1,2

-- Total Cases vs Population --------------------------------------------------------------
-- Shows what percentage of population got COVID ------------------------------------------

-- SELECT location, date, population, total_cases, (total_cases/population)*100 as CovidPercentage
-- FROM coviddeaths
-- WHERE location like '%states%'
-- ORDER BY 1,2

-- Looking at countries with highest infection rate compared to population ---------------

-- SELECT location, population, MAX(total_cases) as HighestInfectionCount, MAX((total_cases/population))*100 as PercentPopulationInfected
-- FROM coviddeaths
-- GROUP BY population, location
-- ORDER BY PercentPopulationInfected DESC

-- Showing countries with highest death count per population -----------------------------

-- SELECT location, MAX(total_deaths) as TotalDeathCount 
-- FROM coviddeaths
-- WHERE location not in ('World', 'European Union', 'Europe','North America', 'Asia', 'Africa', 'South America', 'Oceania', 'International')
-- GROUP BY location
-- ORDER BY TotalDeathCount DESC

-- Global Death Count by Continent -------------------------------------------------------

-- SELECT location, MAX(total_deaths) as TotalDeathCount
-- FROM coviddeaths
-- WHERE location IN ('World', 'European Union', 'Europe','North America', 'Asia', 'Africa', 'South America', 'Oceania', 'International')
-- GROUP BY location
-- ORDER BY TotalDeathCount DESC

-- Global Numbers ------------------------------------------------------------------------

-- SELECT date, SUM(new_cases) as TotalNewCases, SUM(new_deaths) as TotalNewDeaths, (SUM(new_deaths)/SUM(new_cases))*100 as DeathPercentage
-- FROM coviddeaths
-- WHERE location IN ('World', 'European Union', 'Europe','North America', 'Asia', 'Africa', 'South America', 'Oceania', 'International')
-- GROUP BY date
-- ORDER BY 1,2;

-- USE CTE -------------------------------------------------------------------------------
-- Total Population vs Vaccinations ------------------------------------------------------

-- WITH PopvsVac (Continent, Location, Date, Population, New_Vaccinations, RollingPeopleVaccinated) AS 
-- (SELECT d.continent, d.location, d.date, d.population, v.new_vaccinations, 
-- SUM(v.new_vaccinations) OVER(PARTITION BY d.Location ORDER BY d.location, d.date) as RollingPeopleVaccinated
-- FROM coviddeaths d
-- JOIN covidvaccinations v ON d.location = v.location AND d.date = v.date
-- WHERE d.location NOT IN ('World', 'European Union', 'Europe','North America', 'Asia', 'Africa', 'South America', 'Oceania', 'International')
-- )
-- SELECT *, (RollingPeopleVaccinated/Population)*100 AS PercentageVaccinated
-- FROM PopvsVac
-- ORDER BY Location, Date

-- TEMP TABLE ----------------------------------------------------------------------------

-- CREATE TABLE PercentPopulationVaccinated
-- (Continent nvarchar(255),
-- Location nvarchar(255),
-- Date datetime,
-- Population numeric,
-- New_vaccinations numeric,
-- RollingPeopleVaccinated numeric
-- );

-- INSERT INTO PercentPopulationVaccinated
-- SELECT d.continent, d.location, d.date, d.population, v.new_vaccinations, 
-- SUM(v.new_vaccinations) OVER(PARTITION BY d.Location ORDER BY d.location, d.date) as RollingPeopleVaccinated
-- FROM coviddeaths d
-- JOIN covidvaccinations v ON d.location = v.location AND d.date = v.date
-- WHERE d.location NOT IN ('World', 'European Union', 'Europe','North America', 'Asia', 'Africa', 'South America', 'Oceania', 'International');

-- SELECT *, (RollingPeopleVaccinated/Population)*100 AS PercentageVaccinated
-- FROM PercentPopulationVaccinated
-- ORDER BY Location, Date

-- Create View for use later in Data Visualizations ---------------------------------------

-- CREATE VIEW PercentPopulationVaccinatedView AS
-- (SELECT d.continent, d.location, d.date, d.population, v.new_vaccinations, 
-- SUM(v.new_vaccinations) OVER(PARTITION BY d.Location ORDER BY d.location, d.date) as RollingPeopleVaccinated
-- FROM coviddeaths d
-- JOIN covidvaccinations v ON d.location = v.location AND d.date = v.date
-- WHERE d.location NOT IN ('World', 'European Union', 'Europe','North America', 'Asia', 'Africa', 'South America', 'Oceania', 'International'))


