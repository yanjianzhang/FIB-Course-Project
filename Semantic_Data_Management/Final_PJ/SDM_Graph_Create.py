import logging
import sys

from neo4j import GraphDatabase

class App:
    
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    @staticmethod
    def enable_log(level, output_stream):
        handler = logging.StreamHandler(output_stream)
        handler.setLevel(level)
        logging.getLogger("neo4j").addHandler(handler)
        logging.getLogger("neo4j").setLevel(level)
        
        
    ###############
    #Creating nodes
    @staticmethod
    def _load_users(tx):
        print("Loading users...")
        query = (
            "LOAD CSV WITH HEADERS FROM 'file:///users.csv' AS row "
            "CREATE (:User {id: row.reviewerId});"
            )
        tx.run(query)
        print("Users loaded")

    @staticmethod
    def _load_establishments(tx):
        print("Loading establishments...")
        query = (
            "LOAD CSV WITH HEADERS FROM 'file:///establishments.csv' AS row "
            "CREATE (:Establishment {id: row.merge_id, name: row.biz_name});"
            )
        tx.run(query)
        print("Establishments loaded")

    @staticmethod
    def _load_food(tx):
        print("Loading food...")
        query = (
            "LOAD CSV WITH HEADERS FROM 'file:///food.csv' AS row "
            "CREATE (:Food {id: row.tag_id, name: row.food});"
            )
        tx.run(query)
        print("Food loaded")

    @staticmethod
    def _load_cuisine(tx):
        print("Loading cuisine...")
        query = (
            "LOAD CSV WITH HEADERS FROM 'file:///type_cuisine.csv' AS row "
            "CREATE (:Cuisine {id: row.cuisine_id, name: row.cuisine});"
            )
        tx.run(query)
        print("Cuisine loaded")

    @staticmethod
    def _load_atmosphere(tx):
        print("Loading atmosphere...")
        query = (
            "LOAD CSV WITH HEADERS FROM 'file:///atmosphere.csv' AS row "
            "CREATE (:Atmosphere {id: row.atmosphere_id, keyword: row.atmosphere});"
            )
        tx.run(query)
        print("Atmosphere loaded")


        
    ###############
    #Function to load all nodes
    def load_nodes(self):
        with self.driver.session() as session:
            session.write_transaction(self._load_users)

        with self.driver.session() as session:
            session.write_transaction(self._load_establishments)

        with self.driver.session() as session:
            session.write_transaction(self._load_food)

        with self.driver.session() as session:
            session.write_transaction(self._load_atmosphere)

        with self.driver.session() as session:
            session.write_transaction(self._load_cuisine)


    ###############
    #Creating indexes on Ids
    @staticmethod
    def _create_index_userid(tx):
        print("Creating index on User.id...")
        query = ("CREATE INDEX userid_index FOR (n:User) ON (n.id)")
        tx.run(query)
        print("Created index on User.id")
    
    @staticmethod
    def _create_index_establishmentid(tx):
        print("Creating index on Establishment.id...")
        query = ("CREATE INDEX establishmentid_index FOR (n:Establishment) ON (n.id)")
        tx.run(query)
        print("Created index on Establishment.id")

    @staticmethod
    def _create_index_foodid(tx):
        print("Creating index on Food.id...")
        query = ("CREATE INDEX foodid_index FOR (n:Food) ON (n.id)")
        tx.run(query)
        print("Created index on Food.id")

    @staticmethod
    def _create_index_atmosphereid(tx):
        print("Creating index on Atmosphere.id...")
        query = ("CREATE INDEX atmosphereid_index FOR (n:Atmosphere) ON (n.id)")
        tx.run(query)
        print("Created index on Atmosphere.id")

    @staticmethod
    def _create_index_cuisineid(tx):
        print("Creating index on Cuisine.id...")
        query = ("CREATE INDEX cuisineid_index FOR (n:Cuisine) ON (n.id)")
        tx.run(query)
        print("Created index on Cuisine.id")
        

    ###############
    #Function to create indexes
    def create_indexes(self):
        with self.driver.session() as session:
            session.write_transaction(self._create_index_userid)
        
        with self.driver.session() as session:
            session.write_transaction(self._create_index_establishmentid)

        with self.driver.session() as session:
            session.write_transaction(self._create_index_foodid)

        with self.driver.session() as session:
            session.write_transaction(self._create_index_atmosphereid)

        with self.driver.session() as session:
            session.write_transaction(self._create_index_cuisineid)

         

  
    ###############
    #Creating edges
    @staticmethod
    def _load_user_likes_establishment(tx)
    @staticmethod
    def _load_user_likes_food(tx):
        query = (
            "LOAD CSV WITH HEADERS FROM 'file:///user_likes_food.csv' AS row "
            "MATCH (u:User {id: row.reviewerId}), (f:Food {id: row.tag_id})"
            "CREATE (u)-[:LikesFood]->(f);"
            )
        tx.run(query)
        print("Edge (user)-[LIKESFOOD]->(food) loaded")

    @staticmethod
    def _load_user_wants_atmosphere(tx):
        query = (
            "LOAD CSV WITH HEADERS FROM 'file:///user_wants_atmosphere.csv' AS row "
            "MATCH (u:User {id: row.reviewerId}), (a:Atmosphere {id: row.atmosphere_id})"
            "CREATE (u)-[:WantsAtmosphere]->(a);"
            )
        tx.run(query)
        print("Edge (user)-[WANTSATMOSPHERE]->(atmosphere) loaded")

    @staticmethod
    def _load_establishment_hasCuisine(tx):
        query = (
            "LOAD CSV WITH HEADERS FROM 'file:///establishment_has_cuisine.csv' AS row "
            "MATCH (e:Establishment {id: row.merge_id}), (c:Cuisine {id: row.cuisine_id})"
            "CREATE (e)-[:HasCuisine]->(c);"
            )
        tx.run(query)
        print("Edge (establishment)-[HASCUISINE]->(cuisine) loaded")

    @staticmethod
    def _load_establishment_offers_food(tx):
        query = (
            "LOAD CSV WITH HEADERS FROM 'file:///establishment_offers_food.csv' AS row "
            "MATCH (e:Establishment {id: row.merge_id}), (f:Food {id: row.tag_id})"
            "CREATE (e)-[:OffersFood]->(f);"
            )
        tx.run(query)
        print("Edge (establishment)-[OFFERSFOOD]->(food) loaded")

    @staticmethod
    def _load_establishment_hasAtmosphere(tx):
        query = (
            "LOAD CSV WITH HEADERS FROM 'file:///establishment_has_atmosphere.csv' AS row "
            "MATCH (e:Establishment {id: row.merge_id}), (a:Atmosphere {id: row.atmosphere_id})"
            "CREATE (e)-[:HasAtmosphere]->(a);"
            )
        tx.run(query)
        print("Edge (establishment)-[HASATMOSPHERE]->(atmosphere) loaded")


    ###############
    #Function to load all edges
    def load_edges(self):
        with self.driver.session() as session:
            session.write_transaction(self._load_user_likes_food)
        
        with self.driver.session() as session:
            session.write_transaction(self._load_user_isfriendswith_user)

        with self.driver.session() as session:
            session.write_transaction(self._load_user_likes_establishment)

        with self.driver.session() as session:
            session.write_transaction(self._load_user_wants_atmosphere)

        with self.driver.session() as session:
            session.write_transaction(self._load_establishment_hasAtmosphere)

        with self.driver.session() as session:
            session.write_transaction(self._load_establishment_hasCuisine)

        with self.driver.session() as session:
            session.write_transaction(self._load_establishment_offers_food)


if __name__ == "__main__":
    bolt_url = "neo4j://localhost:7687"
    user = "neo4j"
    password = "root"
    App.enable_log(logging.INFO, sys.stdout)
    app = App(bolt_url, user, password)
    app.load_nodes()
    app.create_indexes()
    app.load_edges()
    app.close()