<b>API endpoints:</b>
<br>
<ol>
<b>Block wise list</b>
<ol>
<li>(GET) http://districtdashboard.azurewebsites.net/api/query/blocks?<br>
( Provides list of all indicators with blocks )
<ul>
<li> sector=Health ( Filter by sector )
<li> serial=1.1 ( Filter by serial number of Indicator )
<li> month=5 ( Filter by month of added data )
<li> year=2019 ( Filter by year of added data )
<li> block=Kanke ( Filter by block name )
<li> ranked=True ( Use with serial, month and year to get ranked list of Blocks Indicator wise ) 
</ul>
</ol>
<li> <b> Ranklist </b>
<ol>
<li>(GET) http://districtdashboard.azurewebsites.net/api/query/ranks?<br>
( Provides Ranks and Composite scores of Blocks for given period )
<ul>
<li> block=Kanke ( Get block's rank and composite scores )
<li> month=5 ( Filter by month of added data )
<li> year=2019 ( Filter by year of added data )
</ul>
</ol>
<li> <b>Upload Blockwise data in excel format</b>
<ol>
<li> (POST) http://districtdashboard.azurewebsites.net/api/health/
<ul>
Key = 'health_sheet' Use form-data Multipart with Excel file
</ul>
Uploads data for blocks. Use only specified format 
</ol>
</ol>
