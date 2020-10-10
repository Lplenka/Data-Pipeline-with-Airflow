from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    ui_color = '#F98866'
    
    insert_sql = """
        INSERT INTO {}
        {};
    """

    @apply_defaults
    def __init__(self,
                 table="",
                 redshift_conn_id="",
                 load_sql_stmt="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.load_sql_stmt = load_sql_stmt

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        formatted_sql = LoadFactOperator.insert_sql.format(
            self.table,
            self.load_sql_stmt
        )
        
        self.log.info(f"Loading fact table '{self.table}' into Redshift")
        redshift.run(formatted_sql)
