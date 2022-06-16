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
    # Algorithm
    @staticmethod
    def outdegree_query(tx):
        query = (
            "MATCH (u:User) \
            WITH u.id AS ID, \
             size((u)-[:LikesFood]->()) AS nFood, \
            size((u)-[:likesEstablishment]->()) AS nEstablishment, \
            size((u)-[:WantsAtmosphere]->()) AS nAtmosphere \
            RETURN ID,(nFood+nEstablishment+nAtmosphere) AS OUTDEGREE ORDER BY OUTDEGREE DESC"
            )
        result = tx.run(query)
        # print top 10 line
        count = 0
        for line in result:
            print(line)
            count += 1
            if count >= 10: break
        print("Outdegree Finish")
    
    @staticmethod
    def similarity_query(tx):
        query = (
            "CALL gds.graph.create('E_based_on_A',  \
        ['Establishment', 'Atmosphere'], 'HasAtmosphere')"
            )
        tx.run(query)
        query = (
            "CALL gds.graph.create('E_based_on_C', \
        ['Establishment', 'Cuisine'], 'HasCuisine'); \
   "
            )
        tx.run(query)
        query = (
            "CALL gds.nodeSimilarity.stream('E_based_on_A') \
            YIELD node1, node2, similarity \
            WITH gds.util.asNode(node1).name AS from_A, \
            gds.util.asNode(node2).name AS to_A, \
            similarity AS similarity_A \
            CALL gds.nodeSimilarity.stream('E_based_on_C') \
            YIELD node1, node2, similarity \
            WITH gds.util.asNode(node1).name AS from, \
            gds.util.asNode(node2).name AS to, \
            similarity, similarity_A \
            WHERE from=from_A AND to=to_A \
            RETURN from, to, similarity+similarity_A AS sum_similarity \
            ORDER BY sum_similarity DESCENDING"
            )
        result = tx.run(query)
        # print top 10 line
        count = 0
        for line in result:
            print(line)
            count += 1
            if count >= 10: break
        print("Restaurant similarity Finish")
    
    @staticmethod
    def pagerank_query(tx):
        query = (
            "CALL gds.graph.create( \
                'pagerank', \
                'User', \
                'IsFriendsWith', \
                { \
            } \
            )"
            )
        tx.run(query)
        query = (
            "CALL gds.pageRank.stream('pagerank') \
            YIELD nodeId, score \
            WITH gds.util.asNode(nodeId).id AS user_id, score \
            MATCH (u:User)-[:likesEstablishment]->(e:Establishment) \
            WHERE u.id = user_id \
            WITH e AS Establishment,  apoc.agg.maxItems(user_id, score) as maxData \
            RETURN Establishment.name, maxData.items as user_id, maxData.value as user_pagerank_score"
            )
        result = tx.run(query)
        # print top 10 line
        count = 0
        for line in result:
            print(line)
            count += 1
            if count >= 10: break
        print("Influential User Finding Finish")
    


    ###############
    #Function to run queries
    def outdegree(self):
        with self.driver.session() as session:
            session.write_transaction(self.outdegree_query)
    def similarity(self):
        with self.driver.session() as session:
            session.write_transaction(self.similarity_query)
    def pagerank(self):
        with self.driver.session() as session:
            session.write_transaction(self.pagerank_query)

            
            


if __name__ == "__main__":
    bolt_url = "neo4j://localhost:7687"
    user = "neo4j"
    password = "root"
    App.enable_log(logging.INFO, sys.stdout)
    app = App(bolt_url, user, password)
    app.outdegree()
    app.similarity()
    app.pagerank()
    app.close()
