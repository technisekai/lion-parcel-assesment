select
    *
from retail_transaction
where coalesce(deleted_at, updated_at) >= now() - interval 2 hour