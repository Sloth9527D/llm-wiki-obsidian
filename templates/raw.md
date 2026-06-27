---
create_time: <% tp.file.creation_date() %>
ingest_time:
status: <% tp.system.suggester(["skip","ingested","pend"],["skip","ingested","pend"]) %> 
---