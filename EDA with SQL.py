{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<p style=\"text-align:center\">\n",
    "    <a href=\"https://skills.network\" target=\"_blank\">\n",
    "    <img src=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png\" width=\"200\" alt=\"Skills Network Logo\">\n",
    "    </a>\n",
    "</p>\n",
    "\n",
    "<h1 align=center><font size = 5>Assignment: SQL Notebook for Peer Assignment</font></h1>\n",
    "\n",
    "Estimated time needed: **60** minutes.\n",
    "\n",
    "## Introduction\n",
    "Using this Python notebook you will:\n",
    "\n",
    "1.  Understand the Spacex DataSet\n",
    "2.  Load the dataset  into the corresponding table in a Db2 database\n",
    "3.  Execute SQL queries to answer assignment questions \n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Overview of the DataSet\n",
    "\n",
    "SpaceX has gained worldwide attention for a series of historic milestones. \n",
    "\n",
    "It is the only private company ever to return a spacecraft from low-earth orbit, which it first accomplished in December 2010.\n",
    "SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars wheras other providers cost upward of 165 million dollars each, much of the savings is because Space X can reuse the first stage. \n",
    "\n",
    "\n",
    "Therefore if we can determine if the first stage will land, we can determine the cost of a launch. \n",
    "\n",
    "This information can be used if an alternate company wants to bid against SpaceX for a rocket launch.\n",
    "\n",
    "This dataset includes a record for each payload carried during a SpaceX mission into outer space.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Download the datasets\n",
    "\n",
    "This assignment requires you to load the spacex dataset.\n",
    "\n",
    "In many cases the dataset to be analyzed is available as a .CSV (comma separated values) file, perhaps on the internet. Click on the link below to download and save the dataset (.CSV file):\n",
    "\n",
    " <a href=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv\" target=\"_blank\">Spacex DataSet</a>\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting sqlalchemy==1.3.9\n",
      "  Downloading SQLAlchemy-1.3.9.tar.gz (6.0 MB)\n",
      "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m6.0/6.0 MB\u001b[0m \u001b[31m102.9 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0ma \u001b[36m0:00:01\u001b[0m\n",
      "\u001b[?25h  Preparing metadata (setup.py) ... \u001b[?25ldone\n",
      "\u001b[?25hBuilding wheels for collected packages: sqlalchemy\n",
      "  Building wheel for sqlalchemy (setup.py) ... \u001b[?25ldone\n",
      "\u001b[?25h  Created wheel for sqlalchemy: filename=SQLAlchemy-1.3.9-cp311-cp311-linux_x86_64.whl size=1142923 sha256=032ff979709352a1f244106b476e9cb6a4a999cad8fa9ef1f5d4e295c4fd50b4\n",
      "  Stored in directory: /home/jupyterlab/.cache/pip/wheels/3a/7c/1e/12404784a68083eb969f877a1808a1847bab897684b56ddc55\n",
      "Successfully built sqlalchemy\n",
      "Installing collected packages: sqlalchemy\n",
      "  Attempting uninstall: sqlalchemy\n",
      "    Found existing installation: SQLAlchemy 2.0.30\n",
      "    Uninstalling SQLAlchemy-2.0.30:\n",
      "      Successfully uninstalled SQLAlchemy-2.0.30\n",
      "\u001b[31mERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.\n",
      "jupyterhub 4.1.5 requires SQLAlchemy>=1.4, but you have sqlalchemy 1.3.9 which is incompatible.\u001b[0m\u001b[31m\n",
      "\u001b[0mSuccessfully installed sqlalchemy-1.3.9\n"
     ]
    }
   ],
   "source": [
    "!pip install sqlalchemy==1.3.9\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Connect to the database\n",
    "\n",
    "Let us first load the SQL extension and establish a connection with the database\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting ipython-sql\n",
      "  Downloading ipython_sql-0.5.0-py3-none-any.whl.metadata (17 kB)\n",
      "Collecting prettytable (from ipython-sql)\n",
      "  Downloading prettytable-3.11.0-py3-none-any.whl.metadata (30 kB)\n",
      "Requirement already satisfied: ipython in /opt/conda/lib/python3.11/site-packages (from ipython-sql) (8.22.2)\n",
      "Collecting sqlalchemy>=2.0 (from ipython-sql)\n",
      "  Downloading SQLAlchemy-2.0.36-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (9.7 kB)\n",
      "Collecting sqlparse (from ipython-sql)\n",
      "  Downloading sqlparse-0.5.1-py3-none-any.whl.metadata (3.9 kB)\n",
      "Requirement already satisfied: six in /opt/conda/lib/python3.11/site-packages (from ipython-sql) (1.16.0)\n",
      "Requirement already satisfied: ipython-genutils in /opt/conda/lib/python3.11/site-packages (from ipython-sql) (0.2.0)\n",
      "Requirement already satisfied: typing-extensions>=4.6.0 in /opt/conda/lib/python3.11/site-packages (from sqlalchemy>=2.0->ipython-sql) (4.11.0)\n",
      "Requirement already satisfied: greenlet!=0.4.17 in /opt/conda/lib/python3.11/site-packages (from sqlalchemy>=2.0->ipython-sql) (3.0.3)\n",
      "Requirement already satisfied: decorator in /opt/conda/lib/python3.11/site-packages (from ipython->ipython-sql) (5.1.1)\n",
      "Requirement already satisfied: jedi>=0.16 in /opt/conda/lib/python3.11/site-packages (from ipython->ipython-sql) (0.19.1)\n",
      "Requirement already satisfied: matplotlib-inline in /opt/conda/lib/python3.11/site-packages (from ipython->ipython-sql) (0.1.7)\n",
      "Requirement already satisfied: prompt-toolkit<3.1.0,>=3.0.41 in /opt/conda/lib/python3.11/site-packages (from ipython->ipython-sql) (3.0.42)\n",
      "Requirement already satisfied: pygments>=2.4.0 in /opt/conda/lib/python3.11/site-packages (from ipython->ipython-sql) (2.18.0)\n",
      "Requirement already satisfied: stack-data in /opt/conda/lib/python3.11/site-packages (from ipython->ipython-sql) (0.6.2)\n",
      "Requirement already satisfied: traitlets>=5.13.0 in /opt/conda/lib/python3.11/site-packages (from ipython->ipython-sql) (5.14.3)\n",
      "Requirement already satisfied: pexpect>4.3 in /opt/conda/lib/python3.11/site-packages (from ipython->ipython-sql) (4.9.0)\n",
      "Requirement already satisfied: wcwidth in /opt/conda/lib/python3.11/site-packages (from prettytable->ipython-sql) (0.2.13)\n",
      "Requirement already satisfied: parso<0.9.0,>=0.8.3 in /opt/conda/lib/python3.11/site-packages (from jedi>=0.16->ipython->ipython-sql) (0.8.4)\n",
      "Requirement already satisfied: ptyprocess>=0.5 in /opt/conda/lib/python3.11/site-packages (from pexpect>4.3->ipython->ipython-sql) (0.7.0)\n",
      "Requirement already satisfied: executing>=1.2.0 in /opt/conda/lib/python3.11/site-packages (from stack-data->ipython->ipython-sql) (2.0.1)\n",
      "Requirement already satisfied: asttokens>=2.1.0 in /opt/conda/lib/python3.11/site-packages (from stack-data->ipython->ipython-sql) (2.4.1)\n",
      "Requirement already satisfied: pure-eval in /opt/conda/lib/python3.11/site-packages (from stack-data->ipython->ipython-sql) (0.2.2)\n",
      "Downloading ipython_sql-0.5.0-py3-none-any.whl (20 kB)\n",
      "Downloading SQLAlchemy-2.0.36-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.2 MB)\n",
      "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m3.2/3.2 MB\u001b[0m \u001b[31m88.4 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m:00:01\u001b[0m\n",
      "\u001b[?25hDownloading prettytable-3.11.0-py3-none-any.whl (28 kB)\n",
      "Downloading sqlparse-0.5.1-py3-none-any.whl (44 kB)\n",
      "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m44.2/44.2 kB\u001b[0m \u001b[31m4.4 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
      "\u001b[?25hInstalling collected packages: sqlparse, sqlalchemy, prettytable, ipython-sql\n",
      "  Attempting uninstall: sqlalchemy\n",
      "    Found existing installation: SQLAlchemy 1.3.9\n",
      "    Uninstalling SQLAlchemy-1.3.9:\n",
      "      Successfully uninstalled SQLAlchemy-1.3.9\n",
      "Successfully installed ipython-sql-0.5.0 prettytable-3.11.0 sqlalchemy-2.0.36 sqlparse-0.5.1\n"
     ]
    }
   ],
   "source": [
    "!pip install ipython-sql"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "%load_ext sql"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "import csv, sqlite3\n",
    "\n",
    "con = sqlite3.connect(\"my_data1.db\")\n",
    "cur = con.cursor()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "!pip install -q pandas"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "%sql sqlite:///my_data1.db"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "101"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import pandas as pd\n",
    "df = pd.read_csv(\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv\")\n",
    "df.to_sql(\"SPACEXTBL\", con, if_exists='replace', index=False,method=\"multi\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**Note:This below code is added to remove blank rows from table**\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * sqlite:///my_data1.db\n",
      "Done.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "[]"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#DROP THE TABLE IF EXISTS\n",
    "\n",
    "%sql DROP TABLE IF EXISTS SPACEXTABLE;"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * sqlite:///my_data1.db\n",
      "Done.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "[]"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "%sql create table SPACEXTABLE as select * from SPACEXTBL where Date is not null"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Tasks\n",
    "\n",
    "Now write and execute SQL queries to solve the assignment tasks.\n",
    "\n",
    "**Note: If the column names are in mixed case enclose it in double quotes\n",
    "   For Example \"Landing_Outcome\"**\n",
    "\n",
    "### Task 1\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "##### Display the names of the unique launch sites  in the space mission\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * sqlite:///my_data1.db\n",
      "Done.\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<table>\n",
       "    <thead>\n",
       "        <tr>\n",
       "            <th>Date</th>\n",
       "            <th>Time (UTC)</th>\n",
       "            <th>Booster_Version</th>\n",
       "            <th>Launch_Site</th>\n",
       "            <th>Payload</th>\n",
       "            <th>PAYLOAD_MASS__KG_</th>\n",
       "            <th>Orbit</th>\n",
       "            <th>Customer</th>\n",
       "            <th>Mission_Outcome</th>\n",
       "            <th>Landing_Outcome</th>\n",
       "        </tr>\n",
       "    </thead>\n",
       "    <tbody>\n",
       "        <tr>\n",
       "            <td>2010-06-04</td>\n",
       "            <td>18:45:00</td>\n",
       "            <td>F9 v1.0  B0003</td>\n",
       "            <td>CCAFS LC-40</td>\n",
       "            <td>Dragon Spacecraft Qualification Unit</td>\n",
       "            <td>0</td>\n",
       "            <td>LEO</td>\n",
       "            <td>SpaceX</td>\n",
       "            <td>Success</td>\n",
       "            <td>Failure (parachute)</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>2010-12-08</td>\n",
       "            <td>15:43:00</td>\n",
       "            <td>F9 v1.0  B0004</td>\n",
       "            <td>CCAFS LC-40</td>\n",
       "            <td>Dragon demo flight C1, two CubeSats, barrel of Brouere cheese</td>\n",
       "            <td>0</td>\n",
       "            <td>LEO (ISS)</td>\n",
       "            <td>NASA (COTS) NRO</td>\n",
       "            <td>Success</td>\n",
       "            <td>Failure (parachute)</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>2012-05-22</td>\n",
       "            <td>7:44:00</td>\n",
       "            <td>F9 v1.0  B0005</td>\n",
       "            <td>CCAFS LC-40</td>\n",
       "            <td>Dragon demo flight C2</td>\n",
       "            <td>525</td>\n",
       "            <td>LEO (ISS)</td>\n",
       "            <td>NASA (COTS)</td>\n",
       "            <td>Success</td>\n",
       "            <td>No attempt</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>2012-10-08</td>\n",
       "            <td>0:35:00</td>\n",
       "            <td>F9 v1.0  B0006</td>\n",
       "            <td>CCAFS LC-40</td>\n",
       "            <td>SpaceX CRS-1</td>\n",
       "            <td>500</td>\n",
       "            <td>LEO (ISS)</td>\n",
       "            <td>NASA (CRS)</td>\n",
       "            <td>Success</td>\n",
       "            <td>No attempt</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>2013-03-01</td>\n",
       "            <td>15:10:00</td>\n",
       "            <td>F9 v1.0  B0007</td>\n",
       "            <td>CCAFS LC-40</td>\n",
       "            <td>SpaceX CRS-2</td>\n",
       "            <td>677</td>\n",
       "            <td>LEO (ISS)</td>\n",
       "            <td>NASA (CRS)</td>\n",
       "            <td>Success</td>\n",
       "            <td>No attempt</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>2013-09-29</td>\n",
       "            <td>16:00:00</td>\n",
       "            <td>F9 v1.1  B1003</td>\n",
       "            <td>VAFB SLC-4E</td>\n",
       "            <td>CASSIOPE</td>\n",
       "            <td>500</td>\n",
       "            <td>Polar LEO</td>\n",
       "            <td>MDA</td>\n",
       "            <td>Success</td>\n",
       "            <td>Uncontrolled (ocean)</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>2013-12-03</td>\n",
       "            <td>22:41:00</td>\n",
       "            <td>F9 v1.1</td>\n",
       "            <td>CCAFS LC-40</td>\n",
       "            <td>SES-8</td>\n",
       "            <td>3170</td>\n",
       "            <td>GTO</td>\n",
       "            <td>SES</td>\n",
       "            <td>Success</td>\n",
       "            <td>No attempt</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>2014-01-06</td>\n",
       "            <td>22:06:00</td>\n",
       "            <td>F9 v1.1</td>\n",
       "            <td>CCAFS LC-40</td>\n",
       "            <td>Thaicom 6</td>\n",
       "            <td>3325</td>\n",
       "            <td>GTO</td>\n",
       "            <td>Thaicom</td>\n",
       "            <td>Success</td>\n",
       "            <td>No attempt</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>2014-04-18</td>\n",
       "            <td>19:25:00</td>\n",
       "            <td>F9 v1.1</td>\n",
       "            <td>CCAFS LC-40</td>\n",
       "            <td>SpaceX CRS-3</td>\n",
       "            <td>2296</td>\n",
       "            <td>LEO (ISS)</td>\n",
       "            <td>NASA (CRS)</td>\n",
       "            <td>Success</td>\n",
       "            <td>Controlled (ocean)</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>2014-07-14</td>\n",
       "            <td>15:15:00</td>\n",
       "            <td>F9 v1.1</td>\n",
       "            <td>CCAFS LC-40</td>\n",
       "            <td>OG2 Mission 1  6 Orbcomm-OG2 satellites</td>\n",
       "            <td>1316</td>\n",
       "            <td>LEO</td>\n",
       "            <td>Orbcomm</td>\n",
       "            <td>Success</td>\n",
       "            <td>Controlled (ocean)</td>\n",
       "        </tr>\n",
       "    </tbody>\n",
       "</table>"
      ],
      "text/plain": [
       "[('2010-06-04', '18:45:00', 'F9 v1.0  B0003', 'CCAFS LC-40', 'Dragon Spacecraft Qualification Unit', 0, 'LEO', 'SpaceX', 'Success', 'Failure (parachute)'),\n",
       " ('2010-12-08', '15:43:00', 'F9 v1.0  B0004', 'CCAFS LC-40', 'Dragon demo flight C1, two CubeSats, barrel of Brouere cheese', 0, 'LEO (ISS)', 'NASA (COTS) NRO', 'Success', 'Failure (parachute)'),\n",
       " ('2012-05-22', '7:44:00', 'F9 v1.0  B0005', 'CCAFS LC-40', 'Dragon demo flight C2', 525, 'LEO (ISS)', 'NASA (COTS)', 'Success', 'No attempt'),\n",
       " ('2012-10-08', '0:35:00', 'F9 v1.0  B0006', 'CCAFS LC-40', 'SpaceX CRS-1', 500, 'LEO (ISS)', 'NASA (CRS)', 'Success', 'No attempt'),\n",
       " ('2013-03-01', '15:10:00', 'F9 v1.0  B0007', 'CCAFS LC-40', 'SpaceX CRS-2', 677, 'LEO (ISS)', 'NASA (CRS)', 'Success', 'No attempt'),\n",
       " ('2013-09-29', '16:00:00', 'F9 v1.1  B1003', 'VAFB SLC-4E', 'CASSIOPE', 500, 'Polar LEO', 'MDA', 'Success', 'Uncontrolled (ocean)'),\n",
       " ('2013-12-03', '22:41:00', 'F9 v1.1', 'CCAFS LC-40', 'SES-8', 3170, 'GTO', 'SES', 'Success', 'No attempt'),\n",
       " ('2014-01-06', '22:06:00', 'F9 v1.1', 'CCAFS LC-40', 'Thaicom 6', 3325, 'GTO', 'Thaicom', 'Success', 'No attempt'),\n",
       " ('2014-04-18', '19:25:00', 'F9 v1.1', 'CCAFS LC-40', 'SpaceX CRS-3', 2296, 'LEO (ISS)', 'NASA (CRS)', 'Success', 'Controlled (ocean)'),\n",
       " ('2014-07-14', '15:15:00', 'F9 v1.1', 'CCAFS LC-40', 'OG2 Mission 1  6 Orbcomm-OG2 satellites', 1316, 'LEO', 'Orbcomm', 'Success', 'Controlled (ocean)')]"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "%sql SELECT * FROM SPACEXTABLE LIMIT 10"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * sqlite:///my_data1.db\n",
      "Done.\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<table>\n",
       "    <thead>\n",
       "        <tr>\n",
       "            <th>Launch_Site</th>\n",
       "        </tr>\n",
       "    </thead>\n",
       "    <tbody>\n",
       "        <tr>\n",
       "            <td>CCAFS LC-40</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>VAFB SLC-4E</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>KSC LC-39A</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>CCAFS SLC-40</td>\n",
       "        </tr>\n",
       "    </tbody>\n",
       "</table>"
      ],
      "text/plain": [
       "[('CCAFS LC-40',), ('VAFB SLC-4E',), ('KSC LC-39A',), ('CCAFS SLC-40',)]"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "%sql SELECT DISTINCT Launch_Site FROM SPACEXTABLE"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "\n",
    "### Task 2\n",
    "\n",
    "\n",
    "#####  Display 5 records where launch sites begin with the string 'CCA' \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * sqlite:///my_data1.db\n",
      "Done.\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<table>\n",
       "    <thead>\n",
       "        <tr>\n",
       "            <th>Date</th>\n",
       "            <th>Time (UTC)</th>\n",
       "            <th>Booster_Version</th>\n",
       "            <th>Launch_Site</th>\n",
       "            <th>Payload</th>\n",
       "            <th>PAYLOAD_MASS__KG_</th>\n",
       "            <th>Orbit</th>\n",
       "            <th>Customer</th>\n",
       "            <th>Mission_Outcome</th>\n",
       "            <th>Landing_Outcome</th>\n",
       "        </tr>\n",
       "    </thead>\n",
       "    <tbody>\n",
       "        <tr>\n",
       "            <td>2010-06-04</td>\n",
       "            <td>18:45:00</td>\n",
       "            <td>F9 v1.0  B0003</td>\n",
       "            <td>CCAFS LC-40</td>\n",
       "            <td>Dragon Spacecraft Qualification Unit</td>\n",
       "            <td>0</td>\n",
       "            <td>LEO</td>\n",
       "            <td>SpaceX</td>\n",
       "            <td>Success</td>\n",
       "            <td>Failure (parachute)</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>2010-12-08</td>\n",
       "            <td>15:43:00</td>\n",
       "            <td>F9 v1.0  B0004</td>\n",
       "            <td>CCAFS LC-40</td>\n",
       "            <td>Dragon demo flight C1, two CubeSats, barrel of Brouere cheese</td>\n",
       "            <td>0</td>\n",
       "            <td>LEO (ISS)</td>\n",
       "            <td>NASA (COTS) NRO</td>\n",
       "            <td>Success</td>\n",
       "            <td>Failure (parachute)</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>2012-05-22</td>\n",
       "            <td>7:44:00</td>\n",
       "            <td>F9 v1.0  B0005</td>\n",
       "            <td>CCAFS LC-40</td>\n",
       "            <td>Dragon demo flight C2</td>\n",
       "            <td>525</td>\n",
       "            <td>LEO (ISS)</td>\n",
       "            <td>NASA (COTS)</td>\n",
       "            <td>Success</td>\n",
       "            <td>No attempt</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>2012-10-08</td>\n",
       "            <td>0:35:00</td>\n",
       "            <td>F9 v1.0  B0006</td>\n",
       "            <td>CCAFS LC-40</td>\n",
       "            <td>SpaceX CRS-1</td>\n",
       "            <td>500</td>\n",
       "            <td>LEO (ISS)</td>\n",
       "            <td>NASA (CRS)</td>\n",
       "            <td>Success</td>\n",
       "            <td>No attempt</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>2013-03-01</td>\n",
       "            <td>15:10:00</td>\n",
       "            <td>F9 v1.0  B0007</td>\n",
       "            <td>CCAFS LC-40</td>\n",
       "            <td>SpaceX CRS-2</td>\n",
       "            <td>677</td>\n",
       "            <td>LEO (ISS)</td>\n",
       "            <td>NASA (CRS)</td>\n",
       "            <td>Success</td>\n",
       "            <td>No attempt</td>\n",
       "        </tr>\n",
       "    </tbody>\n",
       "</table>"
      ],
      "text/plain": [
       "[('2010-06-04', '18:45:00', 'F9 v1.0  B0003', 'CCAFS LC-40', 'Dragon Spacecraft Qualification Unit', 0, 'LEO', 'SpaceX', 'Success', 'Failure (parachute)'),\n",
       " ('2010-12-08', '15:43:00', 'F9 v1.0  B0004', 'CCAFS LC-40', 'Dragon demo flight C1, two CubeSats, barrel of Brouere cheese', 0, 'LEO (ISS)', 'NASA (COTS) NRO', 'Success', 'Failure (parachute)'),\n",
       " ('2012-05-22', '7:44:00', 'F9 v1.0  B0005', 'CCAFS LC-40', 'Dragon demo flight C2', 525, 'LEO (ISS)', 'NASA (COTS)', 'Success', 'No attempt'),\n",
       " ('2012-10-08', '0:35:00', 'F9 v1.0  B0006', 'CCAFS LC-40', 'SpaceX CRS-1', 500, 'LEO (ISS)', 'NASA (CRS)', 'Success', 'No attempt'),\n",
       " ('2013-03-01', '15:10:00', 'F9 v1.0  B0007', 'CCAFS LC-40', 'SpaceX CRS-2', 677, 'LEO (ISS)', 'NASA (CRS)', 'Success', 'No attempt')]"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "%sql SELECT * FROM SPACEXTABLE WHERE Launch_Site like 'CCA%' LIMIT 5"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 3\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "##### Display the total payload mass carried by boosters launched by NASA (CRS)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * sqlite:///my_data1.db\n",
      "Done.\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<table>\n",
       "    <thead>\n",
       "        <tr>\n",
       "            <th>Total_Payload</th>\n",
       "        </tr>\n",
       "    </thead>\n",
       "    <tbody>\n",
       "        <tr>\n",
       "            <td>45596</td>\n",
       "        </tr>\n",
       "    </tbody>\n",
       "</table>"
      ],
      "text/plain": [
       "[(45596,)]"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "%sql SELECT SUM(PAYLOAD_MASS__KG_) as Total_Payload from SPACEXTABLE WHERE Customer = 'NASA (CRS)'"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 4\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "##### Display average payload mass carried by booster version F9 v1.1\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * sqlite:///my_data1.db\n",
      "Done.\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<table>\n",
       "    <thead>\n",
       "        <tr>\n",
       "            <th>Average_Payload</th>\n",
       "        </tr>\n",
       "    </thead>\n",
       "    <tbody>\n",
       "        <tr>\n",
       "            <td>2534.6666666666665</td>\n",
       "        </tr>\n",
       "    </tbody>\n",
       "</table>"
      ],
      "text/plain": [
       "[(2534.6666666666665,)]"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "%sql SELECT AVG(PAYLOAD_MASS__KG_) as Average_Payload from SPACEXTABLE WHERE Booster_Version like 'F9 v1.1%'"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 5\n",
    "\n",
    "##### List the date when the first succesful landing outcome in ground pad was acheived.\n",
    "\n",
    "\n",
    "_Hint:Use min function_ \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * sqlite:///my_data1.db\n",
      "Done.\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<table>\n",
       "    <thead>\n",
       "        <tr>\n",
       "            <th>First_Date</th>\n",
       "        </tr>\n",
       "    </thead>\n",
       "    <tbody>\n",
       "        <tr>\n",
       "            <td>2015-12-22</td>\n",
       "        </tr>\n",
       "    </tbody>\n",
       "</table>"
      ],
      "text/plain": [
       "[('2015-12-22',)]"
      ]
     },
     "execution_count": 18,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "%sql SELECT MIN(Date) as First_Date FROM SPACEXTABLE WHERE Landing_Outcome = 'Success (ground pad)'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * sqlite:///my_data1.db\n",
      "Done.\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<table>\n",
       "    <thead>\n",
       "        <tr>\n",
       "            <th>Landing_Outcome</th>\n",
       "        </tr>\n",
       "    </thead>\n",
       "    <tbody>\n",
       "        <tr>\n",
       "            <td>Failure (parachute)</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>No attempt</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>Uncontrolled (ocean)</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>Controlled (ocean)</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>Failure (drone ship)</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>Precluded (drone ship)</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>Success (ground pad)</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>Success (drone ship)</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>Success</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>Failure</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>No attempt </td>\n",
       "        </tr>\n",
       "    </tbody>\n",
       "</table>"
      ],
      "text/plain": [
       "[('Failure (parachute)',),\n",
       " ('No attempt',),\n",
       " ('Uncontrolled (ocean)',),\n",
       " ('Controlled (ocean)',),\n",
       " ('Failure (drone ship)',),\n",
       " ('Precluded (drone ship)',),\n",
       " ('Success (ground pad)',),\n",
       " ('Success (drone ship)',),\n",
       " ('Success',),\n",
       " ('Failure',),\n",
       " ('No attempt ',)]"
      ]
     },
     "execution_count": 20,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "%sql select distinct Landing_Outcome from SPACEXTABLE"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 6\n",
    "\n",
    "##### List the names of the boosters which have success in drone ship and have payload mass greater than 4000 but less than 6000\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * sqlite:///my_data1.db\n",
      "Done.\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<table>\n",
       "    <thead>\n",
       "        <tr>\n",
       "            <th>Booster_Version</th>\n",
       "        </tr>\n",
       "    </thead>\n",
       "    <tbody>\n",
       "        <tr>\n",
       "            <td>F9 FT B1022</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>F9 FT B1026</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>F9 FT  B1021.2</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>F9 FT  B1031.2</td>\n",
       "        </tr>\n",
       "    </tbody>\n",
       "</table>"
      ],
      "text/plain": [
       "[('F9 FT B1022',), ('F9 FT B1026',), ('F9 FT  B1021.2',), ('F9 FT  B1031.2',)]"
      ]
     },
     "execution_count": 21,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "%sql SELECT DISTINCT Booster_Version FROM SPACEXTABLE WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ >= 4000 AND PAYLOAD_MASS__KG_ < 6000"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 7\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "##### List the total number of successful and failure mission outcomes\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * sqlite:///my_data1.db\n",
      "Done.\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<table>\n",
       "    <thead>\n",
       "        <tr>\n",
       "            <th>Successes_and_Failures</th>\n",
       "        </tr>\n",
       "    </thead>\n",
       "    <tbody>\n",
       "        <tr>\n",
       "            <td>71</td>\n",
       "        </tr>\n",
       "    </tbody>\n",
       "</table>"
      ],
      "text/plain": [
       "[(71,)]"
      ]
     },
     "execution_count": 22,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "%sql SELECT COUNT(*) as Successes_and_Failures FROM SPACEXTABLE WHERE Landing_Outcome like 'Success%' OR Landing_Outcome like 'Failure%'"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 8\n",
    "\n",
    "\n",
    "\n",
    "##### List the   names of the booster_versions which have carried the maximum payload mass. Use a subquery\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * sqlite:///my_data1.db\n",
      "Done.\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<table>\n",
       "    <thead>\n",
       "        <tr>\n",
       "            <th>Booster_Version</th>\n",
       "        </tr>\n",
       "    </thead>\n",
       "    <tbody>\n",
       "        <tr>\n",
       "            <td>F9 B5 B1048.4</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>F9 B5 B1049.4</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>F9 B5 B1051.3</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>F9 B5 B1056.4</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>F9 B5 B1048.5</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>F9 B5 B1051.4</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>F9 B5 B1049.5</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>F9 B5 B1060.2 </td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>F9 B5 B1058.3 </td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>F9 B5 B1051.6</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>F9 B5 B1060.3</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>F9 B5 B1049.7 </td>\n",
       "        </tr>\n",
       "    </tbody>\n",
       "</table>"
      ],
      "text/plain": [
       "[('F9 B5 B1048.4',),\n",
       " ('F9 B5 B1049.4',),\n",
       " ('F9 B5 B1051.3',),\n",
       " ('F9 B5 B1056.4',),\n",
       " ('F9 B5 B1048.5',),\n",
       " ('F9 B5 B1051.4',),\n",
       " ('F9 B5 B1049.5',),\n",
       " ('F9 B5 B1060.2 ',),\n",
       " ('F9 B5 B1058.3 ',),\n",
       " ('F9 B5 B1051.6',),\n",
       " ('F9 B5 B1060.3',),\n",
       " ('F9 B5 B1049.7 ',)]"
      ]
     },
     "execution_count": 23,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "%sql SELECT DISTINCT Booster_Version FROM SPACEXTABLE WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTABLE)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 9\n",
    "\n",
    "\n",
    "##### List the records which will display the month names, failure landing_outcomes in drone ship ,booster versions, launch_site for the months in year 2015.\n",
    "\n",
    "**Note: SQLLite does not support monthnames. So you need to use  substr(Date, 6,2) as month to get the months and substr(Date,0,5)='2015' for year.**\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * sqlite:///my_data1.db\n",
      "Done.\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<table>\n",
       "    <thead>\n",
       "        <tr>\n",
       "            <th>Month_Name</th>\n",
       "            <th>Landing_Outcome</th>\n",
       "            <th>Booster_Version</th>\n",
       "            <th>Launch_Site</th>\n",
       "        </tr>\n",
       "    </thead>\n",
       "    <tbody>\n",
       "        <tr>\n",
       "            <td>01</td>\n",
       "            <td>Failure (drone ship)</td>\n",
       "            <td>F9 v1.1 B1012</td>\n",
       "            <td>CCAFS LC-40</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>04</td>\n",
       "            <td>Failure (drone ship)</td>\n",
       "            <td>F9 v1.1 B1015</td>\n",
       "            <td>CCAFS LC-40</td>\n",
       "        </tr>\n",
       "    </tbody>\n",
       "</table>"
      ],
      "text/plain": [
       "[('01', 'Failure (drone ship)', 'F9 v1.1 B1012', 'CCAFS LC-40'),\n",
       " ('04', 'Failure (drone ship)', 'F9 v1.1 B1015', 'CCAFS LC-40')]"
      ]
     },
     "execution_count": 30,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "%sql SELECT substr(Date, 6,2) as Month_Name, Landing_Outcome, Booster_Version, Launch_Site FROM SPACEXTABLE WHERE substr(Date,0,5)='2015' and Landing_Outcome = 'Failure (drone ship)'"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 10\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "##### Rank the count of landing outcomes (such as Failure (drone ship) or Success (ground pad)) between the date 2010-06-04 and 2017-03-20, in descending order.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * sqlite:///my_data1.db\n",
      "Done.\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<table>\n",
       "    <thead>\n",
       "        <tr>\n",
       "            <th>Landing_Outcome</th>\n",
       "            <th>Total_Count</th>\n",
       "        </tr>\n",
       "    </thead>\n",
       "    <tbody>\n",
       "        <tr>\n",
       "            <td>No attempt</td>\n",
       "            <td>10</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>Success (drone ship)</td>\n",
       "            <td>5</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>Failure (drone ship)</td>\n",
       "            <td>5</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>Success (ground pad)</td>\n",
       "            <td>3</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>Controlled (ocean)</td>\n",
       "            <td>3</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>Uncontrolled (ocean)</td>\n",
       "            <td>2</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>Failure (parachute)</td>\n",
       "            <td>2</td>\n",
       "        </tr>\n",
       "        <tr>\n",
       "            <td>Precluded (drone ship)</td>\n",
       "            <td>1</td>\n",
       "        </tr>\n",
       "    </tbody>\n",
       "</table>"
      ],
      "text/plain": [
       "[('No attempt', 10),\n",
       " ('Success (drone ship)', 5),\n",
       " ('Failure (drone ship)', 5),\n",
       " ('Success (ground pad)', 3),\n",
       " ('Controlled (ocean)', 3),\n",
       " ('Uncontrolled (ocean)', 2),\n",
       " ('Failure (parachute)', 2),\n",
       " ('Precluded (drone ship)', 1)]"
      ]
     },
     "execution_count": 34,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "%sql SELECT Landing_Outcome, COUNT(*) as Total_Count FROM SPACEXTABLE WHERE Date between '2010-06-04' and '2017-03-20' GROUP BY Landing_Outcome ORDER BY Total_Count DESC "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Reference Links\n",
    "\n",
    "* <a href =\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Labs_Coursera_V5/labs/Lab%20-%20String%20Patterns%20-%20Sorting%20-%20Grouping/instructional-labs.md.html?origin=www.coursera.org\">Hands-on Lab : String Patterns, Sorting and Grouping</a>  \n",
    "\n",
    "*  <a  href=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Labs_Coursera_V5/labs/Lab%20-%20Built-in%20functions%20/Hands-on_Lab__Built-in_Functions.md.html?origin=www.coursera.org\">Hands-on Lab: Built-in functions</a>\n",
    "\n",
    "*  <a  href=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Labs_Coursera_V5/labs/Lab%20-%20Sub-queries%20and%20Nested%20SELECTs%20/instructional-labs.md.html?origin=www.coursera.org\">Hands-on Lab : Sub-queries and Nested SELECT Statements</a>\n",
    "\n",
    "*   <a href=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Module%205/DB0201EN-Week3-1-3-SQLmagic.ipynb\">Hands-on Tutorial: Accessing Databases with SQL magic</a>\n",
    "\n",
    "*  <a href= \"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Module%205/DB0201EN-Week3-1-4-Analyzing.ipynb\">Hands-on Lab: Analyzing a real World Data Set</a>\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Author(s)\n",
    "\n",
    "<h4> Lakshmi Holla </h4>\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Other Contributors\n",
    "\n",
    "<h4> Rav Ahuja </h4>\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<!--\n",
    "## Change log\n",
    "| Date | Version | Changed by | Change Description |\n",
    "|------|--------|--------|---------|\n",
    "| 2024-07-10 | 1.1 |Anita Verma | Changed Version|\n",
    "| 2021-07-09 | 0.2 |Lakshmi Holla | Changes made in magic sql|\n",
    "| 2021-05-20 | 0.1 |Lakshmi Holla | Created Initial Version |\n",
    "-->\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## <h3 align=\"center\"> © IBM Corporation 2021. All rights reserved. <h3/>\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.9"
  },
  "prev_pub_hash": "a5fa84525a820d08c9ec9c9cccf7d39455745aa2be6c2efdd18931346283d2d9"
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
