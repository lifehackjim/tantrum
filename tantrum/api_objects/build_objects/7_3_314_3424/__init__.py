# -*- coding: utf-8 -*-
"""WSDL contents downloaded from Tanium platform server."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

downloaded_on = "2019-06-02 11:30:50.957728"

from_version = "7.3.314.3424"

from_url_path = "/libraries/taniumjs/console.wsdl"

data = """<?xml version="1.0"?>
<!--
   WSDL description of the Tanium SOAP APIs.
   All interfaces are subject to change as we refine and extend our APIs.
   Please see the terms of use for more information.
-->
<!-- Version: 0.0.1 -->
<definitions
  xmlns:typens="urn:TaniumSOAP"
  xmlns:xsd="http://www.w3.org/2001/XMLSchema"
  xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
  xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/"
  xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
  xmlns="http://schemas.xmlsoap.org/wsdl/"
  name="TaniumSOAP"
  targetNamespace="urn:TaniumSOAP">
  <!-- Types -->
  <types>
    <xsd:schema xmlns="urn:TaniumSOAP" targetNamespace="urn:TaniumSOAP">
      <xsd:complexType name="TaniumSOAPResult">
        <xsd:all>
          <xsd:element name="command"       type="command"        minOccurs="0"/>
          <xsd:element name="auth"          type="auth"           minOccurs="0"/>
          <xsd:element name="session"       type="xsd:string"     minOccurs="0"/>
          <xsd:element name="server_version" type="xsd:string"    minOccurs="0"/>
          <xsd:element name="user"          type="user"           minOccurs="0"/>
          <xsd:element name="IDType"        type="xsd:string"     minOccurs="0"/>   <!-- DEPRECATED: Formerly used by GetResultInfo/Data. Replaced by the object_list tag -->
          <xsd:element name="ID"            type="xsd:int"        minOccurs="0"/>   <!-- DEPRECATED: Formerly used by GetResultInfo/Data. Replaced by the object_list tag -->
          <xsd:element name="ContextID"     type="xsd:int"        minOccurs="0"/>   <!-- DEPRECATED: Formerly used by GetResultInfo/Data. Replaced by the options tag -->
          <xsd:element name="object_list"   type="object_list"    minOccurs="0"/>
          <xsd:element name="options"       type="options"        minOccurs="0"/>
          <xsd:element name="ResultXML"     type="xsd:string"     minOccurs="0"/>   <!-- GetResultInfo and GetResultData return their results here.  NOTE: for backward compatibility this tag's name is ResultXML instead of result_xml -->
          <xsd:element name="result_object" type="object_list"    minOccurs="0"/>   <!-- AddObject and GetObject return their results here. -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="TaniumSOAPRequest">
        <xsd:all>
          <xsd:element name="session"       type="xsd:string"     minOccurs="0"/>   <!-- This should be a valid session returned by auth command -->
          <!--
             Commands:
                GetResultInfo: Get result info for each <question>, <saved_question>, <archived_question>, and/or <action> tag specified in the object_list parameter.
                GetResultData: Get result data for each <question>, <saved_question>, <archived_question>, and/or <action> tag specified in the object_list parameter.
                GetMergedResultData: Get result data for each of the <question> and/or <saved_question> objects specified in the object_list parameter and merge them into a single result_set.
                GetSavedQuestions:  Get the list of defined Saved Questions.  DEPRECATED: Use GetObject instead.
                AddObject: Create new object(s) defined by the object_list parameter.  Not all types are implemented yet.
                GetObject: Retrieve all objects whose types and properties match the ones specified in the object_list parameter. For some types, all objects of that type can be
                  retrieved with a single request.
                MoveObject: Move an object to a content_set, specifying the object by ID and only the content_set property by id or name. Content Set Administrator use only.
                TransferObject: Transfer an object to a different user. Administrator use only.
                UpdateObject: Not Yet Implemented. Update the existing object specified in the object_list parameter to have the values specified in the object_list paramater
                DeleteObject: Delete the object(s) specified in the object_list parameter
                UploadFile:  Uses the upload_file object and adds the specified file to the download cache.
                RunPlugin: Runs any plugins specified in the object_list using the arguments defined in the plugin object.
                PreviewLdapSync: Returns users and groups that would be synchronized based on Ldap settings passed in from request
                ImportObject: Import objects
                ExportObject: Export objects
                NewSessionAsExclusiveUserGroup: Return a new session id for the user using the RBAC permissions and
                    management rights of the exclusive user_group identified in the object_list by a user_group with an id.
                    The current user must be a member of the exclusive user_group.
                VerifySignature: Verify the signature of each <verify_signature> tag specified in the object_list parameter.
                  This should be used in place of the signature validation plugin.
          -->
          <xsd:element name="auth"          type="auth"           minOccurs="0"/>
          <xsd:element name="command"       type="command"     minOccurs="0"/>
          <xsd:element name="object_list"   type="object_list"    minOccurs="0"/>
          <!--
            GetResultInfo and GetResultData:
              The GetResult commands are used to retrieve the data reported to the server by the clients in response to Question objects.
              GetResultInfo returns a summary of the data that is available, and GetResultData returns the actual rows of data.
              The object types that can be used as input are as follows:
                <question>: the result data consists of the answers reported by the clients to that specific question.
                <saved_question>: A saved_question can be sent to the clients repeatedly (aka "reissued"), which is done by creating a question object.  The server will
                  select the "best" question object (a combination of most recent and most complete) and return the results of that question.
                <archived_question>: saved_questions can be set to be archived periodically, and whenever a result set is written into the archive database it is assigned
                  an id referred to as the "archived_question_id".  GetResultInfo can be used with a <saved_question> and the sample_* options to retrieve the ids of
                  a number of archived_questions for that saved question.  These can then be used with GetResultData to get the result set from the archive database.
                <action>: the result data consists of the action status reported by the clients for that action.  There is actually a saved_question and question object
                  that is used to retrieve the action status data, and those ids can be retrieved and queried directly, but using the action id has some useful advantages,
                  in particular, if you set the "row counts only" flag then you can retrieve a special "summary" of action status, collated by action status value.
          -->
          <xsd:element name="options"       type="options"        minOccurs="0"/>   <!-- This replaces all of the DEPRECATED tags below, except ID and IDType which are replaced by the object_list tag -->

          <!-- DEPRECATED:  the following tags are deprecated.  They have been replaced by the Options tag -->
          <xsd:element name="ID"            type="xsd:int"        minOccurs="0"/>   <!-- DEPRECATED: Formerly used by GetResultInfo/Data. Replaced by the object_list tag -->
          <xsd:element name="IDType"        type="xsd:string"     minOccurs="0"/>   <!-- DEPRECATED: One of Question, SavedQuestion, ArchivedQuestion, Action. Formerly used by GetResultInfo/Data. Replaced by the object_list tag -->
          <xsd:element name="ContextID"     type="xsd:int"        minOccurs="0"/>
          <!--
             Bit array of flags, mostly for GetResultInfo/Data:
                1: hide errors
                2: include answer times
                4: row counts only, for IDType "Action" selects between action status "summary" and "details"
                8: aggregate over time
                16: include most recent
                32: include hash values
                64: hide "no results"
          -->
          <xsd:element name="Flags"         type="xsd:int"        minOccurs="0"/>
          <xsd:element name="PctDoneLimit"  type="xsd:int"        minOccurs="0"/>
          <!--
             samplefrequency: how far apart each sample should be (in seconds)
             sampleStart: how many samples into the past we should start with (0 == start with the most recent sample)
             sampleCount: how many samples we should examine

             Note: 600 seconds == 10 minutes, 10 minutes * 144 = one day
             Example: 600, 0, 144 means give me the last day at 10 minute resolution.
             Example: 600, 1440, 144 means give me the day starting from 11 days ago to 10 days ago at 10 minute resolution.

             Note: 3600 seconds == 1 hour, 1 hour * 168 = one week
             Example: 3600, 0, 168 means give me the last week at 1 hour resolution.
             Example: 3600, 168, 168 means give me the week before last week at 1 hour resolution.

             Note: if you ask for 168 samples, you may get fewer (if data is not available) but not more
          -->
          <xsd:element name="SampleFrequency" type="xsd:int"      minOccurs="0"/>
          <xsd:element name="SampleStart"     type="xsd:int"        minOccurs="0"/>
          <xsd:element name="SampleCount"     type="xsd:int"        minOccurs="0"/>
          <!--
             you can select a subset of the result data, by specifying RowStart and RowCount, the order is controlled by SortOrder below
          -->
          <xsd:element name="RowStart"        type="xsd:int"        minOccurs="0"/>
          <xsd:element name="RowCount"        type="xsd:int"        minOccurs="0"/>
          <!--
             you can specify the sort order as a comma-separated list of column indices where the first column is column 1.
             a negative number indicates descending sort order.
             Example: "3,-2" means sort by the third column ascending first, and break ties by sorting by the second column descending
          -->
          <xsd:element name="SortOrder"     type="xsd:string"     minOccurs="0"/>
          <xsd:element name="FilterString"  type="xsd:string"     minOccurs="0"/>   <!-- Filter results to only include items that match this regular expression -->
        </xsd:all>
      </xsd:complexType>
      <xsd:simpleType name="command">
        <xsd:restriction base="xsd:string">
          <xsd:enumeration value="AddObject" />
          <xsd:enumeration value="GetObject" />
          <xsd:enumeration value="MoveObject" />
          <xsd:enumeration value="TransferObject" />
          <xsd:enumeration value="UpdateObject" />
          <xsd:enumeration value="DeleteObject" />
          <xsd:enumeration value="GetSavedQuestions" />
          <xsd:enumeration value="GetResultInfo" />
          <xsd:enumeration value="GetResultData" />
          <xsd:enumeration value="GetMergedResultData" />
          <xsd:enumeration value="UploadFile" />
          <xsd:enumeration value="RunPlugin" />
          <xsd:enumeration value="ExportObject" />
          <xsd:enumeration value="ImportObject" />
          <xsd:enumeration value="VerifySignature" />
        </xsd:restriction>
      </xsd:simpleType>
      <xsd:complexType name="auth">
        <xsd:all>
          <!--
            When authentication is successful the <session> element is populated in the resulting XML.
            Subsequent requests need only supply the session.  Each request extends the lifetime of the session.
            In some situations the session ID may change, so after each request the returned session ID should be checked.
            This can also be done in two different ways:
              HTTP Authentication at https://server/auth which will return the SOAP session ID as the body of the response.
              Headers supplied in POST requests:
                username
                password
                domain
                secondary
                session
                as_exclusive_user_group (only along with user/password authentication for a new session)
          -->
          <xsd:element name="username" type="xsd:string" minOccurs="0"/>
          <xsd:element name="password" type="xsd:string" minOccurs="0"/>
          <xsd:element name="domain"   type="xsd:string" minOccurs="0"/>
          <xsd:element name="secondary" type="xsd:string" minOccurs="0"/> <!-- When using an authentication plugin this can be additional information needed to authenticate. (secure token ID/ldap server) -->
          <xsd:element name="as_exclusive_user_group" type="xsd:string" minOccurs="0"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="sensor_query">
        <xsd:all>
          <xsd:element name="platform"      type="xsd:string"     minOccurs="0"/>   <!--  Windows, Linux, Solaris, AIX or Mac. Defaults to Windows. -->
          <xsd:element name="script"        type="xsd:string"     minOccurs="0"/>   <!-- The script that will be executed on the client -->
          <!--
            The script_type specifies how the script will be executed.
            WMIQuery: execute the script as a WMI Query
            BESRelevance: execute the script as a BigFix Relevance expression (using QNA)
            VBScript: execute the script as a VB Script (if platform is Windows then this is the default)
            Powershell: execute the script using PowerShell
            JScript: execute the script using JScript (Windows platform only)
              - Enable UI support with global setting "enable_python_jscript_type_flag"
            Python: execute the script using Python (all platforms but it requires separate dll/.so files to be distributed to the endpoints).
              - Enable UI support with global setting "enable_python_jscript_type_flag"
            UnixShell: execute the script as a shell script, use #! notation to specify a specific shell program, otherwise /bin/sh will be used (if platform is Linux, Solaris, AIX, or Mac, then this is the default).
          -->
          <xsd:element name="script_type"   type="xsd:string"     minOccurs="0"/>
          <xsd:element name="signature"     type="xsd:string"     minOccurs="0"/>   <!-- A value that will be verified if the server license requires signed content -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="sensor_query_list">
        <xsd:sequence>
          <xsd:element name="query"         type="sensor_query"   minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="sensor_subcolumn">
        <xsd:all>
          <xsd:element name="name"          type="xsd:string"     minOccurs="0"/>
          <xsd:element name="index"         type="xsd:int"        minOccurs="0"/>   <!-- The index into to the delimited sensor data represented by this column -->
          <!--
            The value_type specifies how the values are compared.
            String: standard lexicographical comparison (the default)
            Version: values are expected to be version strings, e.g. 9.4.2 is less than 10.1.3
            Numeric: numeric comparison, including decimal, floating point, and scientific notation
            BESDate: values are expected to be valid BES date strings
            IPAddress: values are expected to be IP addresses
            WMIDate: values are expected to be valid WMI date strings
            TimeDiff: values are expected to be an expression of an amount of time, e.g. "2 years, 3 months, 18 days, 4 hours, 22 minutes, and 3.67 seconds" or "4.2 hours" (numeric + "Y|MO|W|D|H|M|S" units)
            DataSize: values are expected to be an expression of an amount of data, e.g. 125MB or 23K or 34.2Gig (numeric + B|K|M|G|T units)
            NumericInteger:  values are expected to be integer numeric values
          -->
          <xsd:element name="value_type"    type="xsd:string"     minOccurs="0"/>
          <xsd:element name="ignore_case_flag" type="xsd:int"     minOccurs="0"/>   <!-- note that unlike most flags, this defaults to true which means case is ignored by default -->
          <xsd:element name="hidden_flag"   type="xsd:int"        minOccurs="0"/>   <!-- if set, then this is an "internal" object that should not be shown to end users -->
          <!-- tags below this line are Not Yet Implemented: -->
          <xsd:element name="exclude_from_parse_flag" type="xsd:int" minOccurs="0"/> <!-- if true, then the string results of this subcolumn will not be matched by the natural language parser -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="sensor_subcolumn_list">
        <xsd:sequence>
          <xsd:element name="subcolumn" type="sensor_subcolumn"   minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="string_hint_list">
        <xsd:sequence>
          <xsd:element name="string_hint" type="xsd:string" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="sensor_list">
        <xsd:sequence>
          <xsd:element name="sensor"   type="sensor"   minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="cache_info" type="cache_info" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="sensor_stat">
        <xsd:all>
            <xsd:element name="id" type="xsd:long" minOccurs="0"/>
            <xsd:element name="name" type="xsd:string" minOccurs="0"/>
            <xsd:element name="what_hash" type="xsd:long" minOccurs="0"/>
            <xsd:element name="count" type="xsd:long" minOccurs="0"/>
            <xsd:element name="real_ms_min" type="xsd:double" minOccurs="0"/>
            <xsd:element name="real_ms_max" type="xsd:double" minOccurs="0"/>
            <xsd:element name="real_ms_avg" type="xsd:double" minOccurs="0"/>
            <xsd:element name="real_ms_std" type="xsd:double" minOccurs="0"/>
            <xsd:element name="user_ms_avg" type="xsd:double" minOccurs="0"/>
            <xsd:element name="user_ms_std" type="xsd:double" minOccurs="0"/>
            <xsd:element name="sys_ms_avg" type="xsd:double" minOccurs="0"/>
            <xsd:element name="sys_ms_std" type="xsd:double" minOccurs="0"/>
            <xsd:element name="read_bytes_avg" type="xsd:double" minOccurs="0"/>
            <xsd:element name="read_bytes_std" type="xsd:double" minOccurs="0"/>
            <xsd:element name="write_bytes_avg" type="xsd:double" minOccurs="0"/>
            <xsd:element name="write_bytes_std" type="xsd:double" minOccurs="0"/>
            <xsd:element name="other_bytes_avg" type="xsd:double" minOccurs="0"/>
            <xsd:element name="other_bytes_std" type="xsd:double" minOccurs="0"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="sensor_stat_list">
        <xsd:sequence>
            <xsd:element name="sensor_stat" type="sensor_stat" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="saved_action_policy">
        <xsd:all>
          <xsd:element name="saved_question_id" type="xsd:long" minOccurs="0"/>
          <xsd:element name="saved_question_group_id" type="xsd:long" minOccurs="0"/> <!-- deprecated, use saved_question_group instead -->
          <xsd:element name="saved_question_group" type="group" minOccurs="0"/>
          <xsd:element name="row_filter_group_id" type="xsd:long" minOccurs="0"/> <!-- deprecated, use row_filter_group instead -->
          <xsd:element name="row_filter_group" type="group" minOccurs="0"/>
          <xsd:element name="max_age" type="xsd:long" minOccurs="0"/> <!-- defaults to saved_action.issue_seconds -->
          <xsd:element name="min_count" type="xsd:int" minOccurs="0"/> <!-- the number of matching machines required to issue the saved_action. Defaults to the global setting policy_default_min_count -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="saved_action_approval"> <!-- For approving actions use AddObject and supply this -->
        <xsd:all>
          <xsd:element name="id"            type="xsd:long"   minOccurs="0"/> <!-- ID of the saved action to be approved -->
          <xsd:element name="name"          type="xsd:string" minOccurs="0"/> <!-- Name of action to be approved.  Not needed if ID is supplied -->
          <xsd:element name="owner_user_id" type="xsd:int" minOccurs="0"/> <!-- Read-only value: The ID of the user that created the saved action. -->
          <xsd:element name="approved_flag" type="xsd:int"    minOccurs="0"/> <!-- Is action approved or not? This uses the posting user to supply the approver name and ID. -->
          <xsd:element name="metadata" type="metadata_list" minOccurs="0"/> <!-- metadata to be used for approval comments.  entries are associated to the saved action being approved -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="saved_action_approval_list">
        <xsd:sequence>
          <xsd:element name="saved_action_approval"   type="saved_action_approval"   minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="saved_action_row_id_list">
        <xsd:sequence>
          <xsd:element name="row_id" type="xsd:long" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="saved_action">
        <xsd:all>
          <xsd:element name="id"                 type="xsd:long"   minOccurs="0"/>
          <xsd:element name="name"               type="xsd:string" minOccurs="0"/>
          <xsd:element name="comment"            type="xsd:string" minOccurs="0"/> <!-- action comment -->
          <xsd:element name="status"             type="xsd:int"    minOccurs="0"/> <!-- Status of saved action: 0 for Enabled, 1 for Disabled, 2 for Deleted -->
          <xsd:element name="issue_seconds"      type="xsd:int"    minOccurs="0"/>
          <xsd:element name="distribute_seconds" type="xsd:int"    minOccurs="0"/>
          <xsd:element name="start_time"         type="xsd:string" minOccurs="0"/> <!-- the date and time when the action became active, empty string or null means "ASAP" -->
          <xsd:element name="end_time"           type="xsd:string" minOccurs="0"/>
          <xsd:element name="package_spec"       type="package_spec" minOccurs="0"/> <!-- The package deployed by this action -->
          <xsd:element name="action_group_id"    type="xsd:long"   minOccurs="0"/> <!-- deprecated, use action_group instead -->
          <xsd:element name="action_group"       type="group"      minOccurs="0"/> <!-- The parent group of machines to target -->
          <xsd:element name="target_group"       type="group"      minOccurs="0"/> <!-- The group of machines to target -->
          <xsd:element name="public_flag"        type="xsd:int"    minOccurs="0"/> <!-- currently unused -->
          <xsd:element name="policy_flag"        type="xsd:int"    minOccurs="0"/> <!-- flag as to whether or not a policy is being used -->
          <xsd:element name="policy"             type="saved_action_policy" minOccurs="0"/> <!-- definition of the policy -->
          <xsd:element name="metadata"           type="metadata_list" minOccurs="0"/>
          <xsd:element name="row_ids"            type="saved_action_row_id_list" minOccurs="0"/>
          <!-- The following is output only information -->
          <xsd:element name="expire_seconds"     type="xsd:int"    minOccurs="0"/> <!-- how long from the start time before the action expires (value is derived from package) -->
          <xsd:element name="user"               type="user"       minOccurs="0"/>
          <xsd:element name="approved_flag"      type="xsd:int"    minOccurs="0"/>
          <xsd:element name="approver"           type="user"       minOccurs="0"/>
          <xsd:element name="issue_count"        type="xsd:int"    minOccurs="0"/>
          <xsd:element name="creation_time"      type="xsd:string" minOccurs="0"/>
          <xsd:element name="next_start_time"    type="xsd:string" minOccurs="0"/>
          <xsd:element name="last_start_time"    type="xsd:string" minOccurs="0"/>
          <xsd:element name="user_start_time"    type="xsd:string" minOccurs="0"/>
          <xsd:element name="last_action"        type="action"     minOccurs="0"/>
          <xsd:element name="cache_row_id"       type="xsd:int"    minOccurs="0"/> <!-- ID used as a unqiue identifier in the response cache. Refer to cache_id in options. -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="saved_action_list">
        <xsd:sequence>
          <xsd:element name="saved_action" type="saved_action" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="cache_info" type="cache_info" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="sensor">
        <xsd:annotation>
            <xsd:appinfo>
                <constants>
                    <constant>
                        <name>WMI_SENSOR</name>
                        <value type="xsd:int">1</value>
                    </constant>
                    <constant>
                        <name>BES_SENSOR</name>
                        <value type="xsd:int">2</value>
                    </constant>
                    <constant>
                        <name>VBS_SENSOR</name>
                        <value type="xsd:int">4</value>
                    </constant>
                    <constant>
                        <name>PSHELL_SENSOR</name>
                        <value type="xsd:int">5</value>
                    </constant>
                    <constant>
                        <name>MULTITYPE_SENSOR</name>
                        <value type="xsd:int">6</value>
                    </constant>
                    <constant>
                        <name>JS_SENSOR</name>
                        <value type="xsd:int">7</value>
                    </constant>
                    <constant>
                        <name>PY_SENSOR</name>
                        <value type="xsd:int">8</value>
                    </constant>
                    <constant>
                        <name>HASH_RESULT</name>
                        <value type="xsd:int">0</value>
                    </constant>
                    <constant>
                        <name>TEXT_RESULT</name>
                        <value type="xsd:int">1</value>
                    </constant>
                    <constant>
                        <name>VERSION_RESULT</name>
                        <value type="xsd:int">2</value>
                    </constant>
                    <constant>
                        <name>NUMERIC_RESULT</name>
                        <value type="xsd:int">3</value>
                    </constant>
                    <constant>
                        <name>BES_DATETIME_RESULT</name>
                        <value type="xsd:int">4</value>
                    </constant>
                    <constant>
                        <name>IP_RESULT</name>
                        <value type="xsd:int">5</value>
                    </constant>
                    <constant>
                        <name>WMI_DATETIME_RESULT</name>
                        <value type="xsd:int">6</value>
                    </constant>
                    <constant>
                        <name>TIMEDIFF_REUSLT</name>
                        <value type="xsd:int">7</value>
                    </constant>
                    <constant>
                        <name>DATASIZE_RESULT</name>
                        <value type="xsd:int">8</value>
                    </constant>
                    <constant>
                        <name>NUMERIC_INTEGER_RESULT</name>
                        <value type="xsd:int">9</value>
                    </constant>
                    <constant>
                        <name>REGEX_RESULT</name>
                        <value type="xsd:int">11</value>
                    </constant>
                </constants>
            </xsd:appinfo>
        </xsd:annotation>
        <xsd:all>
          <!-- The sensor can be specifed by ID, name, or hash -->
          <xsd:element name="id"            type="xsd:long"       minOccurs="0"/>
          <xsd:element name="name"          type="xsd:string"     minOccurs="0"/>
          <xsd:element name="hash"          type="xsd:long"       minOccurs="0"/>
          <xsd:element name="content_set"   type="id_reference"   minOccurs="0"/>
          <xsd:element name="string_count"  type="xsd:long"       minOccurs="0"/>
          <xsd:element name="category"      type="xsd:string"     minOccurs="0"/>
          <xsd:element name="description"   type="xsd:string"     minOccurs="0"/>
          <xsd:element name="queries"       type="sensor_query_list" minOccurs="0"/>
          <xsd:element name="source_id"     type="xsd:int"       minOccurs="0"/>    <!-- the id of the sensor into which the parameters are substituted, if specified, source_hash may be omitted -->
          <xsd:element name="source_hash"   type="xsd:int"       minOccurs="0"/>    <!-- the hash of the sensor into which the parameters are substituted, if specified, source_id may be omitted -->
          <xsd:element name="source_name"   type="xsd:string"    minOccurs="0"/>    <!-- the name of the source sensor, used for ExportObject/ImportObject where IDs will change. Not used for GetObject/UpdateObject -->
          <xsd:element name="parameters"    type="parameter_list" minOccurs="0"/>   <!-- List of parameters to substitute into the source sensor -->
          <xsd:element name="parameter_definition" type="xsd:string" minOccurs="0"/>
          <!--
            The value_type specifies how the values are compared.
            String: standard lexicographical comparison (the default)
            Version: values are expected to be version strings, e.g. 9.4.2 is less than 10.1.3
            Numeric: numeric comparison, including decimal, floating point, and scientific notation
            BESDate: values are expected to be valid BES date strings
            IPAddress: values are expected to be IP addresses
            WMIDate: values are expected to be valid WMI date strings
            TimeDiff: values are expected to be an expression of an amount of time, e.g. "2 years, 3 months, 18 days, 4 hours, 22 minutes, and 3.67 seconds" or "4.2 hours" (numeric + "Y|MO|W|D|H|M|S" units)
            DataSize: values are expected to be an expression of an amount of data, e.g. 125MB or 23K or 34.2Gig (numeric + B|K|M|G|T units)
            NumericInteger:  values are expected to be integer numeric values
          -->
          <xsd:element name="value_type"    type="xsd:string"     minOccurs="0"/>
          <xsd:element name="max_age_seconds" type="xsd:int"      minOccurs="0"/>   <!-- how old a sensor result can be before we consider it invalid, when results are half this old, the sensor will be re-evaluated -->
          <xsd:element name="ignore_case_flag" type="xsd:int"     minOccurs="0"/>   <!-- note that unlike most flags, this defaults to true which means case is ignored by default -->
          <xsd:element name="exclude_from_parse_flag" type="xsd:int" minOccurs="0"/><!-- if true, then the string results of this sensor will not be used by the natural language parser -->
          <xsd:element name="delimiter"     type="xsd:string"     minOccurs="0"/>   <!-- the character(s) used to split the result into subcolumns -->
          <xsd:element name="subcolumns"    type="sensor_subcolumn_list" minOccurs="0"/>
          <xsd:element name="creation_time"   type="xsd:string"    minOccurs="0"/>   <!-- When this was created in the database -->
          <xsd:element name="modification_time" type="xsd:string"  minOccurs="0"/>   <!-- Last time it was modified -->
          <xsd:element name="last_modified_by" type="xsd:string"   minOccurs="0"/>   <!-- name of the user who last modified or created this -->
          <xsd:element name="mod_user"        type="user"          minOccurs="0"/>   <!-- Last user to modify this -->
          <xsd:element name="string_hints" type="string_hint_list" minOccurs="0"/>   <!-- define initial strings to be hashed and added to the string cache for this sensor. -->
          <xsd:element name="preview_sensor_flag" type="xsd:int" minOccurs="0"/><!-- creates/acquires a preview sensor -->
          <xsd:element name="metadata" type="metadata_list" minOccurs="0"/>
          <xsd:element name="hidden_flag"   type="xsd:int" minOccurs="0"/>
          <xsd:element name="keep_duplicates_flag"   type="xsd:int" minOccurs="0"/>     <!-- Starting with 7.2, clients have the ability to preserve duplicate values in sensor results instead of only returning each unique value once.  Turn this flag on to use that new functionality. -->
          <xsd:element name="deleted_flag"   type="xsd:int" minOccurs="0"/>
          <xsd:element name="cache_row_id"  type="xsd:int" minOccurs="0"/> <!-- ID used as a unqiue identifier in the response cache. Refer to cache_id in options. -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="audit_data">
        <xsd:all>
          <xsd:element name="object_id"     type="xsd:int" minOccurs="0" maxOccurs="1"/>
          <xsd:element name="details"       type="xsd:string" minOccurs="0"/>
          <xsd:element name="creation_time"     type="xsd:string" minOccurs="0"/>   <!-- When this was created in the database -->
          <xsd:element name="modification_time" type="xsd:string" minOccurs="0"/>   <!-- Last time it was modified -->
          <xsd:element name="last_modified_by"  type="xsd:string" minOccurs="0"/>   <!-- name of the user who last modified or created this -->
          <xsd:element name="modifier_user_id"     type="xsd:int" minOccurs="0" maxOccurs="1"/>   <!-- id of the user that made the last modification -->
          <xsd:element name="mod_user"      type="user" minOccurs="0" maxOccurs="1"/> <!-- user object of the user that made the last modification -->
          <xsd:element name="type"          type="xsd:int" minOccurs="0" maxOccurs="1"/> <!-- 0 for create, 1 for update, 2 for delete -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="audit_data_list">
        <xsd:sequence>
          <xsd:element name="entry" type="audit_data" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="cache_info" type="cache_info" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="audit_log">
        <xsd:sequence>
          <!--
            When "id" property is not specified:
              return one entry per unique object id by default.
              set "audit_history_size" to any value other than the default value 1
              to retrieve all possible entries, up to limit specified in "max_soap_audit_entries_per_cache"
            When "id" property is specified:
              use option "audit_history_size" to control number of the audit entries (default = 1)
          -->
          <xsd:element name="id"           type="xsd:int"                 minOccurs="0" />
          <!--
            Supported types:
              user_audit, system_setting_audit, sensor_audit, group_audit, white_listed_url_audit, package_spec_audit,
              saved_action_audit, saved_question_audit, content_set_audit, content_set_role_audit, content_set_role_privilege_audit,
              dashboard_audit, dashboard_group_audit, user_group_audit, authentication_audit, plugin_schedule_audit
          -->
          <xsd:element name="type"         type="xsd:string"              minOccurs="1" maxOccurs="1"/>
          <xsd:element name="start_time"   type="xsd:string"              minOccurs="0" maxOccurs="1"/>  <!-- Use to reduce/filter number of entries -->
          <xsd:element name="end_time"     type="xsd:string"              minOccurs="0" maxOccurs="1"/>  <!-- same as start_time -->
          <xsd:element name="entries"      type="audit_data_list"         minOccurs="0" />
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="audit_log_list">
        <xsd:sequence>
          <xsd:element name="audit_log" type="audit_log" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="server">
        <xsd:all>
          <xsd:element name="id"          type="xsd:int" minOccurs="0" maxOccurs="1"/>
          <xsd:element name="name"        type="xsd:string" minOccurs="0" maxOccurs="1"/>
          <xsd:element name="heart_beat"  type="xsd:string" minOccurs="0" maxOccurs="1"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="server_list">
        <xsd:sequence>
          <xsd:element name="server" type="server" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="server_host">
        <xsd:all>
          <xsd:element name="heart_beat_age_in_minute"  type="xsd:int" minOccurs="0"/>
          <xsd:element name="servers" type="server_list" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="server_host_list">
        <xsd:sequence>
          <xsd:element name="server_host" type="server_host" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="metadata_item">
        <xsd:sequence>
          <xsd:element name="name" type="xsd:string"/>
          <xsd:element name="value" type="xsd:string"/>
          <xsd:element name="admin_flag" type="xsd:int" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="metadata_list">
        <xsd:sequence>
          <xsd:element name="item" type="metadata_item" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="filter">
        <xsd:all>
          <xsd:element name="id"            type="xsd:int"        minOccurs="0"/>
          <xsd:element name="sensor"        type="sensor"         minOccurs="0"/>   <!-- when a filter is applied to machines, the value(s) of this sensor are tested -->
          <!--
            The filter operator defines how the value(s) of the items being tested are compared against the value specified in the filter.
            Available operators are:
              HashMatch: the item passes if the hash of its value matches the filter value (this is the default)
              RegexMatch: the item passes if its value matches the regular expression specified in the filter value
              Less, Greater, LessEqual, GreaterEqual, Equal: the item passes if its value is Less, Greater, LessEqual, GreaterEqual, Equal to the filter value
          -->
          <xsd:element name="operator"      type="xsd:string"     minOccurs="0"/>
          <!--
            The value_type specifies how the values are compared.  This does not apply if the operator is HashMatch or RegexMatch.  The default is the result type of the sensor.
            String: standard lexicographical comparison (the default)
            Version: values are expected to be version strings, e.g. 9.4.2 is less than 10.1.3
            Numeric: numeric comparison, including decimal, floating point, and scientific notation
            BESDate: values are expected to be valid BES date strings
            IPAddress: values are expected to be IP addresses
            WMIDate: values are expected to be valid WMI date strings
            TimeDiff: values are expected to be an expression of an amount of time, e.g. "2 years, 3 months, 18 days, 4 hours, 22 minutes, and 3.67 seconds" or "4.2 hours" (numeric + "Y|MO|W|D|H|M|S" units)
            DataSize: values are expected to be an expression of an amount of data, e.g. 125MB or 23K or 34.2Gig (numeric + B|K|M|G|T units)
            NumericInteger:  values are expected to be integer numeric values
          -->
          <xsd:element name="value_type"    type="xsd:string"     minOccurs="0"/>
          <xsd:element name="value"         type="xsd:string"     minOccurs="0"/>   <!-- depending on the operator, this is the regular expression to match, the hash to match, or the value to compare against -->
          <xsd:element name="not_flag"      type="xsd:int"        minOccurs="0"/>   <!-- if set, negate the match -->
          <xsd:element name="max_age_seconds" type="xsd:int"      minOccurs="0"/>   <!-- how old a sensor result can be before we consider it invalid, default is 0 which means to use the max age property of the sensor -->
          <xsd:element name="ignore_case_flag" type="xsd:int"     minOccurs="0"/>   <!-- note that unlike most flags, this defaults to true which means case is ignored by default -->
          <xsd:element name="all_values_flag" type="xsd:int"      minOccurs="0"/>   <!-- if set, a plural item passes the filter only if all of its values pass the filters, by default a plural item passes if any of its values passes -->
          <!--
            If subtring_flag is set then the substring of the item's value specified by substring_start and substring_length is tested instead of the item's value itself
          -->
          <xsd:element name="substring_flag" type="xsd:int"       minOccurs="0"/>
          <xsd:element name="substring_start" type="xsd:int"      minOccurs="0"/>
          <xsd:element name="substring_length" type="xsd:int"     minOccurs="0"/>
          <!--
            If delimiter is not empty, then the item's value is expected to be a list of values separated by the delimiter and the actual value tested will be the
            "sub item" whose index is specified in the delimiter_index.  This is intended to be used in conjunction with the sensor "sub columns" feature.
          -->
          <xsd:element name="delimiter"     type="xsd:string"     minOccurs="0"/>   <!-- currently only a single character delimiter is supported -->
          <xsd:element name="delimiter_index" type="xsd:int"      minOccurs="0"/>
          <!--
            Not Yet Implemented.  The following tags are reserved for future use:
          -->
          <xsd:element name="utf8_flag"     type="xsd:int"        minOccurs="0"/>   <!-- Not Yet Implemented (for UTF8 regular expressions and case sensitivity) -->
          <xsd:element name="aggregation"   type="xsd:string"     minOccurs="0"/>   <!-- Not Yet Implemented (Sum, Average, Minimum, Maximum, Count) -->
          <xsd:element name="all_times_flag" type="xsd:int"       minOccurs="0"/>   <!-- Not Yet Implemented -->
          <xsd:element name="start_time"    type="xsd:string"     minOccurs="0"/>   <!-- Not Yet Implemented (format is yyyy-mm-ddThh:mm:ss, for example: 2012-07-24T12:31:00 ) -->
          <xsd:element name="end_time"      type="xsd:string"     minOccurs="0"/>   <!-- Not Yet Implemented -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="group_list">
        <xsd:sequence>
          <xsd:element name="group" type="group" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="cache_info" type="cache_info" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="filter_list">
        <xsd:sequence>
          <xsd:element name="filter" type="filter" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="id_reference">
        <xsd:all>
          <xsd:element name="id" type="xsd:int" minOccurs="0" maxOccurs="1"/>
          <!-- can optionally be a reference by name on input, when supported -->
          <xsd:element name="name" type="xsd:string" minOccurs="0" maxOccurs="1"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="group">
        <xsd:all>
          <!--
          The membership of a group is calculated by testing each candidate item and either including it or excluding it from the group.
          First, items are checked to see if they are a member of all of the sub_groups (if and_flag is set), or any of the subgroups (if and_flag is not set)
          Second, items are checked to see if they pass all of the filters ( if and_flag is set), or any of the filters (if and_flag is not set)
          If the not_flag is set the members of the group are all the items that would have normally been excluded.
          Note that if no sub_groups are specified, all items are included, and if no filters are specified, all items are included, so an "empty" group means "All"
          -->
          <xsd:element name="id"           type="xsd:int"        minOccurs="0"/>
          <xsd:element name="name"         type="xsd:string"     minOccurs="0"/>   <!-- note that this is optional, and by default Groups are anonymous. Also, if a group is referred to by name, the name must be unique -->
          <xsd:element name="text"         type="xsd:string"     minOccurs="0" omitByDefault="1"/>   <!-- Text, if any, that this group represents. -->
          <xsd:element name="and_flag"     type="xsd:int"        minOccurs="0"/>
          <xsd:element name="not_flag"     type="xsd:int"        minOccurs="0"/>
          <xsd:element name="type"         type="xsd:int"        minOccurs="0"/>
          <xsd:element name="sub_groups"   type="group_list"     minOccurs="0"/>
          <xsd:element name="filters"      type="filter_list"    minOccurs="0"/>
          <xsd:element name="source_id"    type="xsd:int"        minOccurs="0"/>   <!-- source id of group for parameterized groups -->
          <xsd:element name="parameters"   type="parameter_list" minOccurs="0"/>   <!-- List of parameters to substitute into the source group. -->
          <!-- the following elements are not used at creation time... they are essentially "read-only" -->
          <xsd:element name="deleted_flag" type="xsd:int"        minOccurs="0"/>
          <xsd:element name="track_computer_id_flag" type="xsd:int" minOccurs="0"/> <!-- To turn on or off saved question that track computer ID. Named Group Only. -->
          <xsd:element name="track_computer_id_interval" type="xsd:int" minOccurs="0"/> <!-- Use when track_computer_id_flag is on. Default: 4 hours, Min: 1 hour. Named Group Only. -->
          <xsd:element name="saved_question_id" type="xsd:int"  minOccurs="0"/>    <!-- Readonly: id of the saved question that tracks computer ids in this group. Named Group Only. -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="select">
        <xsd:all>
          <!--
            selects can be filtered by a simple filter, or by a group, or both.
            First, items are checked to see if they are a member of all of the sub_groups (if and_flag is set), or any of the sub_groups (if and_flag is not set)
            Second, items are checked to see if they pass all of the filters ( if and_flag is set), or any of the filters (if and_flag is not set)
            If the not_flag is set the members of the group are all the items that would have normally been excluded.
            Note that if no subgroups are specified, all items are included, and if no filters are specified, all items are included
            -->
          <xsd:element name="sensor"      type="sensor"        minOccurs="0"/>   <!-- the sensor whose values will be retrieved -->
          <xsd:element name="filter"      type="filter"        minOccurs="0"/>   <!-- Only values that pass this filter will be retrieved -->
          <xsd:element name="group"       type="group"         minOccurs="0"/>   <!-- Only values that are members of this group will be retrieved. -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="select_list">
        <xsd:sequence>
          <xsd:element name="select" type="select" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="xml_error">
        <xsd:all>
          <xsd:element name="type" type="xsd:string" minOccurs="0"/>  <!-- type of object that generated an error -->
          <xsd:element name="exception" type="xsd:string" minOccurs="0"/> <!-- the exception or failure that occurred -->
          <xsd:element name="error_context" type="xsd:string" minOccurs="0"/> <!-- the xml being generated at the time of the failure -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="error_list">
        <xsd:sequence>
          <xsd:element name="error" type="xml_error" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="cache_info">
        <xsd:all>
          <xsd:element name="cache_id"         type="xsd:long"   minOccurs="0"/> <!-- ID of the cache created by the request -->
          <xsd:element name="page_row_count"   type="xsd:int"    minOccurs="0"/> <!-- Number of rows return in the curreng page -->
          <xsd:element name="filtered_row_count" type="xsd:int"    minOccurs="0"/> <!-- The total number of rows in this cache after filter/sort-->
          <xsd:element name="cache_row_count"  type="xsd:int"    minOccurs="0"/> <!-- The total number of rows in this cache before filter/sort-->
          <xsd:element name="expiration"       type="xsd:string" minOccurs="0"/> <!-- The time that this cache will expire -->
          <xsd:element name="errors"           type="error_list" minOccurs="0"/> <!-- if there was a problem generating the XML errors will be listed here -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="question_list_info">
        <xsd:all>
          <xsd:element name="highest_id"      type="xsd:int"       minOccurs="0"/>
          <xsd:element name="total_count"     type="xsd:int"       minOccurs="0"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="question_list">
        <xsd:sequence>
          <xsd:element name="info"     type="question_list_info" minOccurs="0"/>
          <xsd:element name="question" type="question" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="cache_info" type="cache_info" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="question">
        <xsd:all>
          <!--
            A question object is a list of data to be retrieved (the "selects"), plus a group that defines the set of machines from which the data should be retrieved.
          -->
          <xsd:element name="id"             type="xsd:int"            minOccurs="0"/>
          <xsd:element name="selects"        type="select_list"        minOccurs="0"/>   <!-- List of what data to retrieve -->
          <xsd:element name="context_group"  type="group"              minOccurs="0"/>   <!-- The context in which this question is asked, similar to management_rights_group but not tied to the user/session context, can be used to narrow the group of machines to retrieve data from -->
          <xsd:element name="group"          type="group"              minOccurs="0"/>   <!-- The group of machines to retrieve the data from -->
          <xsd:element name="expire_seconds" type="xsd:int"            minOccurs="0"/>   <!-- how long from now before the question expires (default is 600) -->
          <xsd:element name="skip_lock_flag" type="xsd:int"            minOccurs="0"/>   <!-- if set, clients will ignore the value of the skip_lock client setting. This should rarely, if ever, be enabled. -->
          <!-- the following elements are not used at creation time... they are essentially "read-only" -->
          <xsd:element name="expiration"     type="xsd:string"         minOccurs="0"/>   <!-- the date and time of expiration  (format is yyyy-mm-ddThh:mm:ss, for example: 2012-07-24T12:31:00 )  -->
          <xsd:element name="is_expired"     type="xsd:int"            minOccurs="0"/>   <!-- is the question expired, at the time it was retrieved -->
          <xsd:element name="user"           type="user"               minOccurs="0"/>   <!-- the user that issued this question. The question will only be answered by machines that were members of the user's management rights group when the question was issued -->
          <xsd:element name="management_rights_group" type="group"     minOccurs="0"/>   <!-- The management rights group of the user at the time the question was issued. -->
          <!-- the following elements are derived from the saved question, if this question object is an instance of a saved question -->
          <xsd:element name="name"            type="xsd:string"        minOccurs="0"/>
          <xsd:element name="query_text"      type="xsd:string"        minOccurs="0"/>   <!-- textual representation of the question -->
          <xsd:element name="hidden_flag"     type="xsd:int"           minOccurs="0"/>   <!-- if set, then this is an "internal" object that should not be shown to end users -->
          <xsd:element name="action_tracking_flag"   type="xsd:int"    minOccurs="0"/>   <!-- indicates that this question is intended to track action status history -->
          <xsd:element name="force_computer_id_flag" type="xsd:int"    minOccurs="0"/>   <!-- force question to not be a counting question if only 1 select is present -->
          <xsd:element name="saved_question"  type="saved_question"    minOccurs="0"/>   <!-- saved question associated to question -->
          <xsd:element name="cache_row_id" type="xsd:int" minOccurs="0"/> <!-- ID used as a unqiue identifier in the response cache. Refer to cache_id in options. -->
          <!--
            The following element is used to specify the order in which questions/saved_questions are merged
            when using the GetMergedResultData command. All or none of the questions/saved_questions in the
            object_list must specify an index, and if the index values are specified, they must be contiguous
            and begin with 0 and not include any duplicate values.
          -->
          <xsd:element name="index"          type="xsd:int"            minOccurs="0"/>
          <!--
            The following element is only included on output of question parser results, and is 1 if the question text was canonically (unambiguously) understood
          -->
          <xsd:element name="from_canonical_text" type="xsd:int"            minOccurs="0"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="package_file_template_list">
        <xsd:sequence>
          <xsd:element name="file_template" type="package_file_template" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="package_file_template">
        <xsd:all>
          <xsd:element name="hash"             type="xsd:string" minOccurs="0"/>   <!-- The SHA-256 hash of the contents of the file -->
          <xsd:element name="name"             type="xsd:string" minOccurs="0"/>
          <xsd:element name="source"           type="xsd:string" minOccurs="0"/>   <!-- Where to get the file from, usually a url or unc path -->
          <xsd:element name="download_seconds" type="xsd:int"    minOccurs="0"/>   <!-- How frequently to check the source to see if there is a new version of the file -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="package_file_status">
        <xsd:all>
          <xsd:element name="server_id"   type="xsd:int"    minOccurs="0"/>
          <xsd:element name="server_name" type="xsd:string" minOccurs="0"/>
          <xsd:element name="status"           type="xsd:int"    minOccurs="0"/>
          <xsd:element name="cache_status"     type="xsd:string" minOccurs="0"/>
          <xsd:element name="cache_message"    type="xsd:string" minOccurs="0"/>
          <xsd:element name="bytes_downloaded" type="xsd:int"    minOccurs="0"/>
          <xsd:element name="bytes_total"      type="xsd:int"    minOccurs="0"/>
          <xsd:element name="download_start_time" type="xsd:string" minOccurs="0"/>   <!--  the time download began  -->
          <xsd:element name="last_download_progress_time" type="xsd:string" minOccurs="0"/>   <!--  the last time dowload progress changed  -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="package_file_status_list">
        <xsd:sequence>
          <xsd:element name="status" type="package_file_status" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="package_file_list">
        <xsd:sequence>
          <xsd:element name="file" type="package_file" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="package_file">
        <xsd:all>
          <xsd:element name="id"               type="xsd:int"    minOccurs="0"/>
          <xsd:element name="hash"             type="xsd:string" minOccurs="0"/>   <!-- The SHA-256 hash of the contents of the file -->
          <xsd:element name="name"             type="xsd:string" minOccurs="0"/>
          <xsd:element name="size"             type="xsd:int"    minOccurs="0"/>
          <xsd:element name="source"           type="xsd:string" minOccurs="0"/>   <!-- Where to get the file from, usually a url or unc path -->
          <xsd:element name="download_seconds" type="xsd:int"    minOccurs="0"/>   <!-- How frequently to check the source to see if there is a new version of the file -->
          <xsd:element name="trigger_download" type="xsd:int"    minOccurs="0"/>   <!-- Using the UpdateObject command, with the ID, and this set to 1 will trigger a re-download of this file into the cache. -->
          <!-- the following elements are not used at creation time... they are essentially "read-only" -->
          <!-- The availability of the file on the server. Expected values are:
              CACHED
              UNCACHED
              [ a string begining with ERROR: ]
          -->
          <xsd:element name="cache_status"     type="xsd:string" minOccurs="0"/>
          <!-- The download status of the file. Common values are:
              0 - check cache_status
              2 - in progress
              4 - in progress
              other number less than 100 - error
              200 - complete (check cache_status)
              4xx - HTTP client error
              5xx - HTTP server error
              1xxx - other error
          -->
          <xsd:element name="status"           type="xsd:int"    minOccurs="0"/>
          <xsd:element name="bytes_downloaded" type="xsd:int"    minOccurs="0"/>
          <xsd:element name="bytes_total"      type="xsd:int"    minOccurs="0"/>
          <xsd:element name="download_start_time" type="xsd:string" minOccurs="0"/>   <!--  the time download began  -->
          <xsd:element name="last_download_progress_time" type="xsd:string" minOccurs="0"/>   <!--  the last time dowload progress changed  -->
          <xsd:element name="file_status"      type="package_file_status_list" minOccurs="0"/> <!-- per server summary of the file status -->
          <xsd:element name="deleted_flag"     type="xsd:int"    minOccurs="0"/>   <!-- if set, then this package file has/will been marked as deleted -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="package_spec_list">
        <xsd:sequence>
          <xsd:element name="package_spec" type="package_spec" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="cache_info" type="cache_info" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="package_spec">
        <xsd:all>
          <!--
            A package_spec object is a list of files to be distributed and a command to be executed. Typically referred to simply as a "package"
          -->
          <xsd:element name="id"              type="xsd:long"      minOccurs="0"/>
          <xsd:element name="name"            type="xsd:string"    minOccurs="0"/>   <!-- it is possible to refer to an object by name, but if the name is not unique an error may be generated. -->
          <xsd:element name="content_set"     type="id_reference"  minOccurs="0"/>
          <xsd:element name="display_name"    type="xsd:string"    minOccurs="0"/>   <!-- display name of package -->
          <xsd:element name="files"           type="package_file_list" minOccurs="0"/>  <!-- List of files to distribute -->
          <xsd:element name="file_templates"  type="package_file_template_list" minOccurs="0"/>  <!-- List of files to distribute where file is determined by parameter substitution -->
          <xsd:element name="command"         type="xsd:string"    minOccurs="0"/>   <!-- Command to be executed -->
          <xsd:element name="command_timeout" type="xsd:int"       minOccurs="0"/>   <!-- Limit on how long the command can execute before it will be terminated -->
          <xsd:element name="expire_seconds"  type="xsd:int"       minOccurs="0"/>   <!-- This value is added to the command_timeout to determine how long the action will be active before it is considered expired -->
          <xsd:element name="hidden_flag"     type="xsd:int"       minOccurs="0"/>   <!-- if set, then this is an "internal" object that should not be shown to end users.
                                                                                          This normally defaults to false; however, if source_id is specified, it defaults to true.  -->
          <xsd:element name="process_group_flag" type="xsd:int"    minOccurs="0"/>   <!-- if set, then 7.1+ clients will run the package command in a process group. This setting has no effect on pre-7.1 clients.
                                                                                          The client will also kill any remaining descendant processes when the package command completes.
                                                                                          This defaults to false. -->
          <xsd:element name="signature"       type="xsd:string"    minOccurs="0"/>   <!-- A value that will be verified if the server license requires signed content -->
          <xsd:element name="source_id"       type="xsd:int"       minOccurs="0"/>   <!-- the package id of the package into which the parameters are substituted -->
          <xsd:element name="source_name"     type="xsd:string"    minOccurs="0"/>   <!-- the name of the source package, used for ExportObject/ImportObject where IDs will change. Not used for GetObject/UpdateObject -->
          <!--
            The "source_hash" is used to detect whether the derived package is out of sync with the source package.
            The "source_hash_changed_flag" is only applicable to derived packages.
            - For source package: the hash representation of current state of the source package, and it can change when certain properties of this package are modified.
            - For non-source package: the hash is copied from the source package at creation time and will not change.
          -->
          <xsd:element name="source_hash"     type="xsd:string"       minOccurs="0"/>
          <xsd:element name="source_hash_changed_flag"  type="xsd:int"  minOccurs="0"/>
          <xsd:element name="verify_group_id" type="xsd:int"       minOccurs="0"/>   <!-- deprecated, use verify_group -->
          <xsd:element name="verify_group"    type="group"         minOccurs="0"/>   <!-- use this to specify a verify group. this will create one if it doesn't exist -->
          <xsd:element name="verify_expire_seconds" type="xsd:int" minOccurs="0"/>
          <xsd:element name="skip_lock_flag"  type="xsd:int"       minOccurs="0"/>
          <xsd:element name="parameters"      type="parameter_list" minOccurs="0"/>  <!-- List of parameters to substitute into the source package -->
          <xsd:element name="parameter_definition" type="xsd:string" minOccurs="0"/>
          <xsd:element name="sensors"              type="sensor_list" minOccurs="0" /> <!-- sensors associated with a particular package -->
          <!-- following elements are not used at creation time... they are essentially "read-only" -->
          <xsd:element name="creation_time"   type="xsd:string"    minOccurs="0"/>   <!-- When this was created in the database -->
          <xsd:element name="modification_time" type="xsd:string"  minOccurs="0"/>   <!-- Last time it was modified -->
          <xsd:element name="last_modified_by" type="xsd:string"   minOccurs="0"/>   <!-- name of the user who last modified or created this -->
          <xsd:element name="mod_user"        type="user"          minOccurs="0"/>   <!-- Last user to modify this -->
          <xsd:element name="available_time"  type="xsd:string"    minOccurs="0"/>   <!-- the date and time when all of the files became available -->
          <xsd:element name="deleted_flag"    type="xsd:int"       minOccurs="0"/>   <!-- if set, then this package has been marked as deleted -->
          <xsd:element name="metadata"        type="metadata_list" minOccurs="0"/>
          <xsd:element name="last_update"     type="xsd:string"    minOccurs="0"/>   <!-- the date and time when this package was last updated -->
          <xsd:element name="cache_row_id"    type="xsd:int"       minOccurs="0"/> <!-- ID used as a unqiue identifier in the response cache. Refer to cache_id in options. -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="client_status">
        <xsd:all>
          <!--
            A client_status object is details about a client at the last time it reported.
          -->
          <xsd:element name="host_name"         type="xsd:string"          minOccurs="0"/>
          <xsd:element name="computer_id"       type="xsd:string"          minOccurs="0"/>
          <xsd:element name="ipaddress_client"  type="xsd:string"          minOccurs="0"/>
          <xsd:element name="ipaddress_server"  type="xsd:string"          minOccurs="0"/>
          <xsd:element name="protocol_version"  type="xsd:int"             minOccurs="0"/>
          <xsd:element name="full_version"      type="xsd:string"          minOccurs="0"/>
          <xsd:element name="last_registration" type="xsd:string"          minOccurs="0"/>
          <xsd:element name="send_state"        type="xsd:string"          minOccurs="0"/>
          <xsd:element name="receive_state"     type="xsd:string"          minOccurs="0"/>
          <xsd:element name="status"            type="xsd:string"          minOccurs="0"/>
          <xsd:element name="port_number"       type="xsd:int"             minOccurs="0"/>
          <xsd:element name="public_key_valid"  type="xsd:int"             minOccurs="0"/>
          <xsd:element name="registered_with_tls" type="xsd:int"           minOccurs="0"/>

          <xsd:element name="cache_row_id" type="xsd:int" minOccurs="0"/> <!-- ID used as a unqiue identifier in the response cache. Refer to cache_id in options. -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="system_setting">
        <xsd:all>
          <xsd:element name="id"             type="xsd:int"    minOccurs="0"/>
          <xsd:element name="name"           type="xsd:string" minOccurs="0"/>
          <xsd:element name="value"          type="xsd:string" minOccurs="0"/>
          <xsd:element name="default_value"  type="xsd:string" minOccurs="0"/>
          <xsd:element name="value_type"     type="xsd:string" minOccurs="0"/> <!-- value_type is either Text or Numeric -->
          <xsd:element name="setting_type"   type="xsd:string" minOccurs="0"/> <!-- setting_type is either Server or Client -->
          <xsd:element name="hidden_flag"    type="xsd:int"    minOccurs="0"/>
          <xsd:element name="read_only_flag" type="xsd:int"    minOccurs="0"/>
          <xsd:element name="audit_data"     type="audit_data" minOccurs="0"/>
          <xsd:element name="metadata"       type="metadata_list" minOccurs="0"/>

          <xsd:element name="cache_row_id" type="xsd:int" minOccurs="0"/> <!-- ID used as a unqiue identifier in the response cache. Refer to cache_id in options. -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="soap_error">
        <xsd:all>
          <xsd:element name="object_name"    type="xsd:string"    minOccurs="0"/>
          <xsd:element name="exception_name" type="xsd:string"    minOccurs="0"/>
          <xsd:element name="context"        type="xsd:string"    minOccurs="0"/>
          <xsd:element name="object_request" type="xsd:string"    minOccurs="0"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="white_listed_url">
        <xsd:all>
          <xsd:element name="id"               type="xsd:int"       minOccurs="0"/>
          <xsd:element name="chunk_id"         type="xsd:string"    minOccurs="0"/>
          <xsd:element name="download_seconds" type="xsd:int"       minOccurs="0"/>   <!-- How frequently to check the source to see if there is a new version of the file -->
          <xsd:element name="expire_seconds"   type="xsd:int"       minOccurs="0"/>   <!-- How long after a client requests this download that it can be cleaned up until requested again. 0 indicates never expire. -->
          <xsd:element name="metadata"         type="metadata_list" minOccurs="0"/>
          <xsd:element name="url_regex"        type="xsd:string"    minOccurs="0"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="white_listed_url_list">
        <xsd:sequence>
          <xsd:element name="white_listed_url" type="white_listed_url" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="version_aggregate">
        <xsd:sequence>
          <xsd:element name="version_string" type="xsd:string" minOccurs="0"/>
          <xsd:element name="count"          type="xsd:int"    minOccurs="0"/>
          <xsd:element name="filtered"       type="xsd:int"    minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="version_aggregate_list">
        <xsd:sequence>
          <xsd:element name="version" type="version_aggregate" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="system_status_aggregate">
        <xsd:sequence>
          <xsd:element name="send_forward_count"     type="xsd:int"/>
          <xsd:element name="send_backward_count"    type="xsd:int"/>
          <xsd:element name="send_none_count"        type="xsd:int"/>
          <xsd:element name="send_ok_count"          type="xsd:int"/>
          <xsd:element name="receive_forward_count"  type="xsd:int"/>
          <xsd:element name="receive_backward_count" type="xsd:int"/>
          <xsd:element name="receive_none_count"     type="xsd:int"/>
          <xsd:element name="receive_ok_count"       type="xsd:int"/>
          <xsd:element name="slowlink_count"         type="xsd:int"/>
          <xsd:element name="blocked_count"          type="xsd:int"/>
          <xsd:element name="leader_count"           type="xsd:int"/>
          <xsd:element name="normal_count"           type="xsd:int"/>
          <xsd:element name="registered_with_tls_count" type="xsd:int"/>
          <xsd:element name="versions"               type="version_aggregate_list"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="system_status_list">
        <xsd:sequence>
          <xsd:element name="client_status" type="client_status" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="aggregate" type="system_status_aggregate" minOccurs="0"/>
          <xsd:element name="cache_info" type="cache_info" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="system_setting_list">
        <xsd:sequence>
          <xsd:element name="system_setting" type="system_setting" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="cache_info" type="cache_info" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="user_list">
        <xsd:sequence>
          <xsd:element name="user" type="user" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <!-- Legacy pre-7.1 permission constants -->
      <xsd:complexType name="permission_list">
        <xsd:annotation>
          <xsd:appinfo>
            <constants>
              <constant>
                  <name>ADMIN</name>
                  <value type="xsd:string">admin</value>
              </constant>
              <constant>
                  <name>QUESTION_READ</name>
                  <value type="xsd:string">question_read</value>
              </constant>
              <constant>
                  <name>QUESTION_WRITE</name>
                  <value type="xsd:string">question_write</value>
              </constant>
              <constant>
                  <name>SENSOR_READ</name>
                  <value type="xsd:string">sensor_read</value>
              </constant>
              <constant>
                  <name>SENSOR_WRITE</name>
                  <value type="xsd:string">sensor_write</value>
              </constant>
              <constant>
                  <name>ACTION_READ</name>
                  <value type="xsd:string">action_read</value>
              </constant>
              <constant>
                  <name>ACTION_WRITE</name>
                  <value type="xsd:string">action_write</value>
              </constant>
              <constant>
                  <name>ACTION_APPROVE</name>
                  <value type="xsd:string">action_approval</value>
              </constant>
              <constant>
                  <name>NOTIFICATION_WRITE</name>
                  <value type="xsd:string">notification_write</value>
              </constant>
              <constant>
                  <name>CLIENTS_READ</name>
                  <value type="xsd:string">clients_read</value>
              </constant>
              <constant>
                  <name>QUESTION_LOG_READ</name>
                  <value type="xsd:string">question_log_read</value>
              </constant>
              <constant>
                  <name>CONTENT_ADMIN</name>
                  <value type="xsd:string">content_admin</value>
              </constant>
            </constants>
          </xsd:appinfo>
        </xsd:annotation>
        <xsd:sequence>
            <xsd:element name="permission" type="xsd:string" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="user_role">
        <xsd:all>
          <xsd:element name="id" type="xsd:int" minOccurs="0"/>
          <xsd:element name="name" type="xsd:string" minOccurs="0"/>
          <xsd:element name="description" type="xsd:string" minOccurs="0"/>
          <xsd:element name="permissions" type="permission_list" minOccurs="0"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="user_role_list">
        <xsd:sequence>
          <xsd:element name="role" type="user_role" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="user_owned_object_ids">
        <xsd:all>
          <xsd:element name="saved_actions" type="saved_action_list" minOccurs="0"/>
          <xsd:element name="saved_questions" type="saved_question_list" minOccurs="0"/>
          <xsd:element name="plugin_schedules" type="plugin_schedule_list" minOccurs="0"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="user">
        <xsd:all>
          <xsd:element name="id"                      type="xsd:int"          minOccurs="0"/>
          <xsd:element name="name"                    type="xsd:string"       minOccurs="0"/>   <!-- it is possible to refer to an object by name, but if the name is not unique an error may be generated. -->
          <xsd:element name="domain"                  type="xsd:string"       minOccurs="0"/>   <!-- domain of user -->
          <xsd:element name="display_name"            type="xsd:string"       minOccurs="0"/>   <!-- display name -->
          <xsd:element name="permissions"             type="permission_list"  minOccurs="0"/>   <!-- list of enabled permissions, read-only as it comes from the user's role and content_set_user_groups -->
          <xsd:element name="roles"                   type="user_role_list"   minOccurs="0"     omitByDefault="1"/>   <!-- roles this user is a member of -->
          <xsd:element name="group_id"                type="xsd:int"          minOccurs="0"/>   <!-- user's management rights group ID -->
          <xsd:element name="effective_group_id"      type="xsd:int"          minOccurs="0"     omitByDefault="1"/> <!-- user's effective management rights group ID - user and user groups -->
          <xsd:element name="deleted_flag"            type="xsd:int"          minOccurs="0"/>   <!-- is the user deleted or not -->
          <xsd:element name="last_login"              type="xsd:string"       minOccurs="0"/>   <!-- the date and time of the most recent login by this user -->
          <xsd:element name="active_session_count"    type="xsd:int"          minOccurs="0"/>   <!-- the number of active sessions for this user -->
          <xsd:element name="local_admin_flag"        type="xsd:int"          minOccurs="0"/>
          <xsd:element name="locked_out"              type="xsd:int"          minOccurs="0"/>   <!-- is the user locked out by LDAP sync or not -->
          <xsd:element name="metadata" type="metadata_list" minOccurs="0"/>
          <!-- for add/update only, can be used to replace the content_set_role_membership objects for this user -->
          <xsd:element name="content_set_roles" type="content_set_role_list" minOccurs="0"      omitByDefault="1"/>
          <!-- for the current user from include_user_details only -->
          <xsd:element name="effective_content_set_privileges"        type="effective_content_set_privilege_list"     minOccurs="0"      omitByDefault="1"/>
          <!-- Administrator only. Used to shown content IDs that this user owns. Use with "include_user_owned_object_ids_flag" option -->
          <xsd:element name="owned_object_ids"        type="user_owned_object_ids"     minOccurs="0"      omitByDefault="1"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="action_list_info">
        <xsd:all>
          <xsd:element name="highest_id"      type="xsd:int"       minOccurs="0"/>
          <xsd:element name="total_count"     type="xsd:int"       minOccurs="0"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="action_list">
        <xsd:sequence>
          <xsd:element name="info" type="action_list_info" minOccurs="0"/>
          <xsd:element name="action" type="action" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="cache_info" type="cache_info" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="action">
        <xsd:all>
          <!--
            An action object is a package to be deployed, plus a group that defines the set of machines to be deployed to (the target).
          -->
          <xsd:element name="id"              type="xsd:long"       minOccurs="0"/>
          <xsd:element name="name"            type="xsd:string"    minOccurs="0"/>   <!-- it is possible to refer to an object by name, but if the name is not unique an error may be generated. -->
          <xsd:element name="comment"         type="xsd:string"    minOccurs="0"/>
          <xsd:element name="target_group"    type="group"         minOccurs="0"/>   <!-- The group of machines to target -->
          <xsd:element name="action_group"    type="group"         minOccurs="0"/>   <!-- The parent group of machines to target -->
          <xsd:element name="package_spec"    type="package_spec"  minOccurs="0"/>   <!-- The package deployed by this action -->
          <xsd:element name="start_time"      type="xsd:string"    minOccurs="0"/>   <!-- the date and time when the action became active, empty string or null means "ASAP" -->
          <xsd:element name="expiration_time" type="xsd:string"    minOccurs="0"/>   <!-- the date and time when the action will expire -->
          <xsd:element name="status"          type="xsd:string"    minOccurs="0"/>   <!-- Status of action: Pending/Active/Stopped/Expired -->
          <xsd:element name="skip_lock_flag"  type="xsd:int"       minOccurs="0"/>
          <!-- following elements are not used at creation time... they are essentially "read-only" -->
          <xsd:element name="expire_seconds"  type="xsd:int"       minOccurs="0"/>   <!-- how long from the start time before the action expires (value is derived from package) -->
          <xsd:element name="distribute_seconds" type="xsd:int"    minOccurs="0"/>
          <xsd:element name="creation_time"   type="xsd:string"    minOccurs="0"/>   <!-- the date and time of creation of the object in the database -->
          <xsd:element name="stopped_flag"    type="xsd:int"       minOccurs="0"/>   <!-- whether an action stop has been issued for this action -->
          <xsd:element name="user"            type="user"          minOccurs="0"/>   <!-- the user that issued this action -->
          <xsd:element name="approver"        type="user"          minOccurs="0"/>   <!-- If there is an approver this will be populated. -->
          <xsd:element name="history_saved_question" type="saved_question" minOccurs="0"/>  <!-- the saved question that tracks the results of the action -->
          <xsd:element name="saved_action"    type="saved_action"  minOccurs="0"/>   <!-- saved action this action was issued from -->
          <xsd:element name="metadata"        type="metadata_list" minOccurs="0"/> <!-- metadata output only, it is loaded from the related saved action -->
          <xsd:element name="cache_row_id" type="xsd:int" minOccurs="0"/> <!-- ID used as a unqiue identifier in the response cache. Refer to cache_id in options. -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="action_stop_list">
        <xsd:sequence>
          <xsd:element name="action_stop" type="action_stop" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="action_stop">
        <xsd:all>
          <!--
            An action stop object causes the given action (identified by its id) to be stopped
          -->
          <xsd:element name="id"              type="xsd:int"       minOccurs="0"/>
          <xsd:element name="action"          type="action"        minOccurs="0"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="archived_question_list">
        <xsd:sequence>
          <xsd:element name="archived_question" type="archived_question" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="archived_question">
        <xsd:all>
          <xsd:element name="id"              type="xsd:int"       minOccurs="0"/>   <!-- the unique id of this object.  This is the preferred way to refer to an object. -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="saved_question_list">
        <xsd:sequence>
          <xsd:element name="saved_question" type="saved_question" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="cache_info" type="cache_info" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="saved_question">
        <xsd:all>
          <xsd:element name="id"              type="xsd:int"       minOccurs="0"/>   <!-- the unique id of this object.  This is the preferred way to refer to an object. -->
          <xsd:element name="name"            type="xsd:string"    minOccurs="0"/>   <!-- it is possible to refer to an object by name, but if the name is not unique an error may be generated. -->
          <xsd:element name="content_set"     type="id_reference"  minOccurs="0"/>
          <xsd:element name="question"        type="question"      minOccurs="0"/>   <!-- When adding a saved_question object, you must include a question object -->
          <!--
            For creation only. If set, server will populate the initial result data from those specified questions.
            Useful for copying recent data from one saved question, or from multipe questions, to this saved question, to create the recent data set.
            Seeding questions must:
            - have the same group right as the defintion question
            - have the force_computer_id_flag = 1, same for the defintion questoin
            - have at least one overlapping column with the defintion question
            You must trigger reissue right after saved question creation for this to work.
          -->
          <xsd:element name="seeding_question_ids"  type="xsd:string" minOccurs="0"/>
          <xsd:element name="public_flag"     type="xsd:int"       minOccurs="0"/>   <!-- if false, then only the user that owns this object should be allowed to use/see it -->
          <xsd:element name="hidden_flag"     type="xsd:int"       minOccurs="0"/>   <!-- if set, then this is an "internal" object that should not be shown to end users -->
          <xsd:element name="issue_seconds"   type="xsd:int"       minOccurs="0"/>   <!-- how often to reissue the question when active (default is 120) -->
          <xsd:element name="issue_seconds_never_flag" type="xsd:int" minOccurs="0"/><!-- indicates that this question is never reissued automatically -->
          <xsd:element name="expire_seconds"  type="xsd:int"       minOccurs="0"/>   <!-- how long before each issuance of the question expires (default is 600) -->
          <xsd:element name="sort_column"     type="xsd:int"       minOccurs="0"/>   <!-- which column to use as the default sort column if no sort_order is specified -->
          <xsd:element name="query_text"      type="xsd:string"    minOccurs="0"/>   <!-- textual representation of the question -->
          <xsd:element name="packages"        type="package_spec_list"  minOccurs="0"/>   <!-- the packages associated with this saved question and available to be deployed -->
          <!--
            The following tags relate to the archiving of result data in order to track results of a saved question over time.
          -->
          <xsd:element name="row_count_flag"  type="xsd:int"       minOccurs="0"/>   <!-- indicates that only the row count data should be saved when archiving this question -->
          <xsd:element name="keep_seconds"    type="xsd:int"       minOccurs="0"/>   <!-- how often to save result data into the archive -->
          <xsd:element name="archive_enabled_flag" type="xsd:int" minOccurs="0"/>    <!-- indicates whether archiving is enabled -->
          <xsd:element name="skip_schedule_on_update_flag" type="xsd:int" minOccurs="0"/>    <!-- indicates whether to create or update existing reissue schedule on UpdateObject command call. This is also used internally by MoveObject command. -->
          <!-- following elements are not used at creation time... they are essentially "read-only" -->
          <xsd:element name="most_recent_question_id" type="xsd:int" minOccurs="0"/> <!-- the id of the most recently issued question object generated by this saved_question -->
          <xsd:element name="user"            type="user"          minOccurs="0"/>   <!-- the user that owns this object -->
          <xsd:element name="archive_owner"   type="user"          minOccurs="0"/>   <!-- the user that owns the archive. Archives can be shared between users with identical management rights groups -->
          <xsd:element name="action_tracking_flag" type="xsd:int"  minOccurs="0"/>   <!-- indicates that this question is intended to track action status history -->
          <xsd:element name="mod_time"        type="xsd:string"    minOccurs="0"/>   <!-- Last time this was modified -->
          <xsd:element name="mod_user"        type="user"          minOccurs="0"/>   <!-- Last user to modify this -->
          <xsd:element name="metadata"        type="metadata_list" minOccurs="0"/>
          <!--
            The following element is used to specify the order in which questions/saved_questions are merged
            when using the GetMergedResultData command. All or none of the questions/saved_questions in the
            object_list must specify an index, and if the index values are specified, they must be contiguous
            and begin with 0 and not include any duplicate values.
          -->
          <xsd:element name="index"          type="xsd:int"            minOccurs="0"/>
          <xsd:element name="cache_row_id" type="xsd:int" minOccurs="0"/> <!-- ID used as a unqiue identifier in the response cache. Refer to cache_id in options. -->
        </xsd:all>
      </xsd:complexType>
      <!--
            Adding a parse_job object will return a list of parse_result_groups, each of which corresponds to a possible question object that might match the question_text of the parse_job.
            Adding a parse_result_group object will create the corresponding question object and issue it, returning a question id.
      -->
      <xsd:complexType name="parse_job_list">
        <xsd:sequence>
          <xsd:element name="parse_job" type="parse_job" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="parse_job">
        <xsd:all>
          <xsd:element name="question_text"         type="xsd:string" minOccurs="0"/>
          <xsd:element name="parser_version"        type="xsd:int" minOccurs="0"/>   <!-- defaults to 0
                                                                                          Version 0 == old parser returning parse_results
                                                                                          Version 1 == old parser returning questions
                                                                                          Version 2 == new parser returning questions, with failover to old parser returning questions if new parser fails/times out
                                                                                          Version 3 == new parser returning questions, no failover -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="parse_result_group_list">
        <xsd:sequence>
          <xsd:element name="parse_result_group" type="parse_result_group" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="parse_result_list">
        <xsd:sequence>
          <xsd:element name="parse_result" type="parse_result" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="parameter_list">
        <xsd:sequence>
          <xsd:element name="parameter" type="parameter" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="parameter">
        <xsd:all>
          <xsd:element name="key"    type="xsd:string" minOccurs="0"/>
          <xsd:element name="value"  type="xsd:string" minOccurs="0"/>
          <xsd:element name="type"   type="xsd:int"    minOccurs="0"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="parse_result">
        <xsd:all>
          <xsd:element name="id"                type="xsd:int"        minOccurs="0"/>
          <xsd:element name="parameters"        type="parameter_list" minOccurs="0"/>
          <xsd:element name="parameter_definition"  type="xsd:string"     minOccurs="0"/>
        </xsd:all>
      </xsd:complexType>
        <xsd:complexType name="parameter_value_list">
            <xsd:sequence>
                <xsd:element name="value" type="xsd:string" minOccurs="0"/>
            </xsd:sequence>
        </xsd:complexType>
        <xsd:complexType name="sensor_reference">
            <xsd:all>
                <xsd:element name="name" type="xsd:string"/>
                <xsd:element name="start_char" type="xsd:int"/>
                <xsd:element name="real_ms_avg" type="xsd:int"/>
            </xsd:all>
        </xsd:complexType>
        <xsd:complexType name="sensor_reference_list">
            <xsd:sequence>
                <xsd:element name="sensor_reference" type="sensor_reference" minOccurs="0"/>
            </xsd:sequence>
        </xsd:complexType>
      <xsd:complexType name="parse_result_group">
        <xsd:all>
          <xsd:element name="score"                  type="xsd:int"           minOccurs="0"/>
          <xsd:element name="question_text"          type="xsd:string"        minOccurs="0"/>
          <xsd:element name="parse_results"          type="parse_result_list" minOccurs="0"/>    <!-- Version 0 returns these -->
          <xsd:element name="question"               type="question"          minOccurs="0"/>    <!-- Later versions return these instead of parse_results -->
          <xsd:element name="question_group_sensors" type="sensor_list"       minOccurs="0"/>    <!-- Later versions include this extra data to help with parameterization -->
          <xsd:element name="parameter_values"       type="parameter_value_list" minOccurs="0"/> <!-- 7.2 and later will strip parameters and return them here, left to right order -->
          <xsd:element name="sensor_references"      type="sensor_reference_list" minOccurs="0"/> <!-- 7.3 and later will return sensor names and start char in question text -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="client_count">
          <xsd:all>
            <xsd:element name="count"          type="xsd:int"           minOccurs="0"/>
          </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="plugin_argument">
        <xsd:all>
          <xsd:element name="name" type="xsd:string" minOccurs="0"/>
          <xsd:element name="type" type="xsd:string" minOccurs="0"/>
          <xsd:element name="value" type="xsd:string" minOccurs="0"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="plugin_argument_list">
          <xsd:sequence>
            <xsd:element name="argument" type="plugin_argument" minOccurs="0" maxOccurs="unbounded"/>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="plugin_sql_result_list">
        <xsd:sequence>
          <xsd:element name="value" type="xsd:string" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="plugin_sql_column_list">
        <xsd:sequence>
          <xsd:element name="name" type="xsd:string" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="plugin_sql">
        <xsd:sequence>
          <xsd:element name="columns" type="plugin_sql_column_list"/>
          <xsd:element name="result_row" type="plugin_sql_result_list" maxOccurs="unbounded"/>
          <xsd:element name="rows_affected" type="xsd:long" minOccurs="0"/>
          <xsd:element name="result_count" type="xsd:long" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="plugin_command_list">
          <xsd:sequence>
            <xsd:element name="command" type="xsd:string" minOccurs="0" maxOccurs="unbounded"/>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="upload_file">
        <xsd:all>
          <xsd:element name="id" type="xsd:int" minOccurs="0"/> <!-- When an upload is started this will be populated with the ID, use for subsequent upload chunks -->
          <xsd:element name="key" type="xsd:string" minOccurs="0"/> <!-- Associate a unique identifer with a file upload.  This will be returned with each response. -->
          <xsd:element name="destination_file" type="xsd:string" minOccurs="0"/> <!-- If this file is not meant for the download cache you can supply a name here. -->
          <xsd:element name="hash" type="xsd:string" minOccurs="0"/> <!-- The expected SHA-256 or SHA-512. If empty the hash will not be verified. On file completion this will be populated with the resulting hash of the file.-->
          <xsd:element name="force_overwrite" type="xsd:int" minOccurs="0"/> <!-- If a file already exists overwrite it with this upload. -->
          <xsd:element name="file_size" type="xsd:long" minOccurs="0"/> <!-- The size of the complete file. -->
          <xsd:element name="start_pos" type="xsd:long" minOccurs="0"/> <!-- The position in the file where this chunk of bytes starts -->
          <xsd:element name="bytes" type="xsd:string" minOccurs="0"/> <!-- the base64 encoded bytes for the entire file or part of the file -->
            <!-- Elements returned for information only -->
          <xsd:element name="file_cached" type="xsd:int" minOccurs="0"/> <!-- If the file is complete and has been moved to the download cache this will be true -->
          <xsd:element name="part_size" type="xsd:int" minOccurs="0"/> <!-- This is the size of the requested part. -->
          <xsd:element name="percent_complete" type="xsd:int" minOccurs="0"/> <!-- Percent complete of file. -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="upload_file_list">
          <xsd:sequence>
            <xsd:element name="upload_file" type="upload_file" minOccurs="0" maxOccurs="unbounded"/>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="upload_file_status">
        <xsd:all>
          <xsd:element name="hash" type="xsd:string" minOccurs="0"/> <!-- The expected SHA-256 of the completed file. -->
          <xsd:element name="percent_complete" type="xsd:int" minOccurs="0"/> <!-- Percent complete of file. -->
          <xsd:element name="file_cached" type="xsd:int" minOccurs="0"/> <!-- If the file is complete and has been moved to the download cache this will be true -->
          <xsd:element name="file_parts" type="upload_file_list" minOccurs="0"/> <!-- returns the details of each uploaded file part -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="plugin">
        <xsd:annotation>
            <xsd:appinfo>
                <constants>
                    <constant>
                        <name>SQL</name>
                        <value type="xsd:string">SQL</value>
                    </constant>
                    <constant>
                        <name>SCRIPT</name>
                        <value type="xsd:string">Script</value>
                    </constant>
                </constants>
            </xsd:appinfo>
        </xsd:annotation>
        <xsd:all>
          <xsd:element name="name"             type="xsd:string"/>
          <xsd:element name="bundle"           type="xsd:string"           minOccurs="0"/> <!-- which bundle this plugin is a part of. Essentially the namespace -->
          <xsd:element name="plugin_server"    type="xsd:string"           minOccurs="0"/> <!-- in the case where multiple plugin servers exist this can specify which one should run the plugin. -->
          <xsd:element name="input"            type="xsd:string"           minOccurs="0"/> <!-- If the plugin is a script this is what is passed to the stdin of that script -->
          <xsd:element name="arguments"        type="plugin_argument_list" minOccurs="0"/> <!-- if this is a SQL plugin these will be the arguments supplied to the query -->
          <xsd:element name="sql_response"     type="plugin_sql"           minOccurs="0"/>  <!-- If the plugin is a SQL type this will be populated in the response object. -->
          <xsd:element name="script_response"  type="xsd:string"           minOccurs="0"/>  <!-- If the plugin is a script type this will be populated in the response object. -->
          <xsd:element name="exit_code"        type="xsd:int"              minOccurs="0"/> <!-- if the plugin is a script type the exit code will be here. -->
          <xsd:element name="type"             type="xsd:string"           minOccurs="0"/> <!-- plugin type: SQL/Script.  Return data only. -->
          <xsd:element name="metadata"         type="metadata_list"        minOccurs="0"/> <!-- associated metadata.  Return data only. -->
          <xsd:element name="path"             type="xsd:string"           minOccurs="0"/> <!-- the path the commands will be executed on and where the definition file resides -->
          <xsd:element name="filename"         type="xsd:string"           minOccurs="0"/> <!-- The filename that contains the plugin definition -->
          <xsd:element name="plugin_url"       type="xsd:string"           minOccurs="0"/> <!-- If this is a remote plugin this will be the URI for accessing it.  For example: /plugin/foo/bar -->
          <xsd:element name="commands"         type="plugin_command_list"  minOccurs="0"/> <!-- list of commands run by the plugin -->
          <xsd:element name="permissions"      type="permission_list"      minOccurs="0"/> <!-- list of permissions required to use this plugin -->
          <xsd:element name="run_detached_flag" type="xsd:int"             minOccurs="0"/> <!-- This plugin execution request will respond immediately running the plugin in the background. -->
          <xsd:element name="execution_id"     type="xsd:int"              minOccurs="0"/> <!-- If this is a detached plugin request this will have the ID used to look up the results. If this is supplied in a GetObject request the status will be returned. -->
          <xsd:element name="timeout_seconds"  type="xsd:int"              minOccurs="0"/> <!-- The maximum run-time of a plugin, defaults to 10 seconds. -->
          <xsd:element name="cache_row_id"     type="xsd:int"              minOccurs="0"/> <!-- ID used as a unqiue identifier in the response cache. Refer to cache_id in options. -->
          <xsd:element name="local_admin_flag" type="xsd:int"              minOccurs="0"/>
          <xsd:element name="allow_rest"       type="xsd:int"              minOccurs="0"/>
          <xsd:element name="raw_http_response" type="xsd:int"             minOccurs="0"/>
          <xsd:element name="raw_http_request" type="xsd:int"              minOccurs="0"/>
          <xsd:element name="use_json_flag"    type="xsd:int"              minOccurs="0"/>
          <xsd:element name="content_set"      type="content_set"          minOccurs="0"/>
          <!-- When calling RunPlugin and supplying a valid execution_id these fields will be populated. -->
          <xsd:element name="status"           type="xsd:string"           minOccurs="0"/> <!-- The status of the plugin execution: Not Started, Running, Completed, Failed. -->
          <xsd:element name="status_file_content" type="xsd:string"        minOccurs="0"/> <!-- The contents of the status file if supplied in run request. -->
          <!-- The status file location is stored in the environment variable PLUGIN_STATUS_FILE. Any plugins that want content here should populate that file.-->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="plugin_list">
          <xsd:sequence>
            <xsd:element name="plugin" type="plugin" minOccurs="0" maxOccurs="unbounded"/>
            <xsd:element name="cache_info" type="cache_info" minOccurs="0"/>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="plugin_schedule">
        <xsd:all>
          <!-- When a plugin schedule is added it will execute the specified plugin based on this criteria.  Each execution will be run as the user that created the schedule -->
          <xsd:element name="id"                   type="xsd:int"              minOccurs="0"/>
          <xsd:element name="name"                 type="xsd:string"           minOccurs="0"/> <!-- name of this schedule.  Used as an identifier. -->
          <xsd:element name="plugin_name"          type="xsd:string"           minOccurs="0"/>
          <xsd:element name="plugin_bundle"        type="xsd:string"           minOccurs="0"/>
          <xsd:element name="plugin_server"        type="xsd:string"           minOccurs="0"/>
          <xsd:element name="start_hour"           type="xsd:int"              minOccurs="0"/> <!-- if supplied the schedule will only run between start_hour and end_hour: 0 ~ 23 -->
          <xsd:element name="end_hour"             type="xsd:int"              minOccurs="0"/>
          <xsd:element name="start_date"           type="xsd:string"              minOccurs="0"/> <!-- if supplied the schedule will only run after the specified date -->
          <xsd:element name="end_date"             type="xsd:string"              minOccurs="0"/> <!-- if supplied the schedule will only run until the specified date -->
          <xsd:element name="run_on_days"          type="xsd:string"           minOccurs="0"/> <!-- If supplied plugin will only run on specified days separated by commas.  As: Mon, Tue, Wed, Thu, Fri, Sat, Sun. -->
          <xsd:element name="run_interval_seconds" type="xsd:int"              minOccurs="0"/> <!-- the interval between executions of the plugin. -->
          <xsd:element name="enabled"              type="xsd:int"              minOccurs="0"/> <!-- Whether or not this schedule is enabled. 1 or 0. -->
          <xsd:element name="deleted_flag"         type="xsd:int"              minOccurs="0"/> <!-- Whether or not this schedule is deleted. 1 or 0. -->
          <xsd:element name="input"                type="xsd:string"           minOccurs="0"/> <!-- If the plugin is a script this is what is passed to the stdin of that script -->
          <xsd:element name="arguments"            type="plugin_argument_list" minOccurs="0"/> <!-- if this is a SQL plugin these will be the arguments supplied to the query -->
          <xsd:element name="user"                 type="user"                 minOccurs="0"/> <!-- Read Only: The user the plugin will run as -->
          <xsd:element name="last_run_time"        type="xsd:string"           minOccurs="0"/> <!-- Read Only: The last time this was run -->
          <xsd:element name="last_exit_code"       type="xsd:int"              minOccurs="0"/> <!-- Read Only: Exit code of last run. -->
          <xsd:element name="last_run_text"        type="xsd:string"           minOccurs="0"/> <!-- Read Only: If the plugin is not SQL this will have the output. -->
          <xsd:element name="last_run_sql"         type="plugin_sql"           minOccurs="0"/> <!-- Read Only: SQL output if applicable. -->
          <xsd:element name="modification_time"    type="xsd:string"           minOccurs="0"/>
          <xsd:element name="mod_user"        type="user"          minOccurs="0"/>   <!-- Last user to modify this -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="plugin_schedule_list">
          <xsd:sequence>
            <xsd:element name="plugin_schedule" type="plugin_schedule" minOccurs="0" maxOccurs="unbounded"/>
            <xsd:element name="cache_info" type="cache_info" minOccurs="0"/>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="computer_group_spec">
        <xsd:sequence>
          <xsd:element name="id" type="xsd:int" minOccurs="0"/>
          <xsd:element name="computer_name" type="xsd:string" minOccurs="0"/>
          <xsd:element name="ip_address"    type="xsd:string" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="computer_spec_list">
        <xsd:sequence>
          <xsd:element name="computer_spec" type="computer_group_spec" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="cache_info"    type="cache_info"          minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="computer_group">
        <xsd:sequence>
          <xsd:element name="id"             type="xsd:int"            minOccurs="0"/>
          <xsd:element name="name"           type="xsd:string"         minOccurs="0"/>
          <xsd:element name="deleted_flag"   type="xsd:int"            minOccurs="0"/>
          <xsd:element name="computer_specs" type="computer_spec_list" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="computer_group_list">
        <xsd:sequence>
          <xsd:element name="computer_group" type="computer_group" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="cache_info"     type="cache_info"     minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="verify_signature">
        <xsd:sequence>
          <xsd:element name="id" type="xsd:int" minOccurs="0"/> <!-- the id of this object.  This is the preferred way to be sure that the answer correspond to this request. -->
          <xsd:element name="type" type="xsd:string" minOccurs="0"/> <!-- the type of data to verify: console, content, or manifest -->
          <xsd:element name="bytes" type="xsd:string" minOccurs="0"/> <!-- the base64 encoded bytes for the entire file -->
          <xsd:element name="verified" type="xsd:string" minOccurs="0"/> <!-- Read Only: 1 or 0, depending if the signature was verified or not -->
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="object_list">
        <xsd:sequence>
          <!--
            Which of the following tags is allowed, and how many of them, depends on the Command specified in the request.
            GetResultInfo: Expects one of question, saved_question, archived_question, action.  See comments for ID and IDType above for details.
            GetResultData: Expects one of question, saved_question, archived_question, action.  See comments for ID and IDType above for details.
            GetSavedQuestions:  Ignores this tag
            AddObject: Expects one or more of question, parse_job, parse_result_group, group, action, action_stop, package_spec, sensor, saved_question.  user is planned, but Not Yet Implemented
            GetObject: Expects one or more of question, group, action, action_stop, package_spec, sensor, saved_question.  user is planned, but Not Yet Implemented
            UpdateObject: Not Yet Implemented
            DeleteObject: Expects one or more of group, saved_question, package_spec, sensor.
          -->
          <xsd:element name="question"            type="question"                minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="questions"           type="question_list"           minOccurs="0"/>
          <xsd:element name="group"               type="group"                   minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="groups"              type="group_list"              minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="saved_question"      type="saved_question"          minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="saved_questions"     type="saved_question_list"     minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="archived_question"   type="archived_question"       minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="archived_questions"  type="archived_question_list"  minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="parse_job"           type="parse_job"               minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="parse_jobs"          type="parse_job_list"          minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="parse_result_group"  type="parse_result_group"      minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="parse_result_groups" type="parse_result_group_list" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="action"              type="action"                  minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="actions"             type="action_list"             minOccurs="0"/>
          <xsd:element name="saved_action"        type="saved_action"            minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="saved_actions"       type="saved_action_list"       minOccurs="0"/>
          <xsd:element name="action_stop"         type="action_stop"             minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="action_stops"        type="action_stop_list"        minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="package_spec"        type="package_spec"            minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="package_specs"       type="package_spec_list"       minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="package_file"        type="package_file"            minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="package_files"       type="package_file_list"       minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="sensor"              type="sensor"                  minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="sensors"             type="sensor_list"             minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="user"                type="user"                    minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="users"               type="user_list"               minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="user_group"          type="user_group"              minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="user_groups"         type="user_group_list"         minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="solution"            type="solution"                minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="solutions"           type="solution_list"           minOccurs="0"/>
          <xsd:element name="action_group"        type="action_group"            minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="action_groups"       type="action_group_list"       minOccurs="0"/>
          <!-- roles is present in taniumjs only for talking to older servers - removed in 7.1 -->
          <xsd:element name="roles"               type="user_role_list"          minOccurs="0"/>
          <xsd:element name="client_status"       type="client_status"           minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="system_setting"      type="system_setting"          minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="saved_action_approval" type="saved_action_approval" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="saved_action_approvals" type="saved_action_approval_list" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="system_status"       type="system_status_list"      minOccurs="0"/>
          <xsd:element name="system_settings"     type="system_setting_list"    minOccurs="0"/>
          <xsd:element name="client_count"        type="client_count"            minOccurs="0"/>
          <xsd:element name="plugin"              type="plugin"                  minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="plugins"             type="plugin_list"             minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="plugin_schedule"     type="plugin_schedule"         minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="plugin_schedules"    type="plugin_schedule_list"    minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="white_listed_url"    type="white_listed_url"        minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="white_listed_urls"   type="white_listed_url_list"   minOccurs="0"/>
          <xsd:element name="upload_file"         type="upload_file"             minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="upload_file_status"  type="upload_file_status"      minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="sensor_stat"         type="sensor_stat"             minOccurs="0"/>
          <xsd:element name="sensor_stats"        type="sensor_stat_list"        minOccurs="0"/>
          <xsd:element name="soap_error"          type="soap_error"              minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="computer_groups"     type="computer_group_list"     minOccurs="0"/>
          <xsd:element name="computer_group"      type="computer_group"          minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="export_id"           type="xsd:string"              minOccurs="0"/>
          <xsd:element name="server_info"         type="xsd:string"              minOccurs="0"/>
          <xsd:element name="content_set"         type="content_set"              minOccurs="0"/>
          <xsd:element name="content_sets"        type="content_set_list"              minOccurs="0"/>
          <xsd:element name="content_set_privilege"            type="content_set_privilege"             minOccurs="0"/>
          <xsd:element name="content_set_privileges"           type="content_set_privilege_list"        minOccurs="0"/>
          <xsd:element name="content_set_role"                 type="content_set_role"                  minOccurs="0"/>
          <xsd:element name="content_set_roles"                type="content_set_role_list"             minOccurs="0"/>
          <xsd:element name="content_set_role_membership"      type="content_set_role_membership"       minOccurs="0"/>
          <xsd:element name="content_set_role_memberships"     type="content_set_role_membership_list"  minOccurs="0"/>
          <xsd:element name="content_set_role_privilege"       type="content_set_role_privilege"        minOccurs="0"/>
          <xsd:element name="content_set_role_privileges"      type="content_set_role_privilege_list"   minOccurs="0"/>
          <xsd:element name="content_set_user_group_role_membership"  type="content_set_user_group_role_membership"       minOccurs="0"/>
          <xsd:element name="content_set_user_group_role_memberships" type="content_set_user_group_role_membership_list"  minOccurs="0"/>
          <xsd:element name="effective_content_set_privileges"        type="effective_content_set_privilege_request"         minOccurs="0"/>
          <xsd:element name="saved_question_package_specs"     type="saved_question_package_specs"  minOccurs="0"/>
          <xsd:element name="saved_question_question"          type="saved_question_question"  minOccurs="0"/>
          <xsd:element name="saved_question_questions"         type="saved_question_question_list"  minOccurs="0"/>
          <xsd:element name="audit_log"                        type="audit_log"              minOccurs="0"/>
          <xsd:element name="audit_logs"                       type="audit_log_list"             minOccurs="0"/>
          <xsd:element name="server_host"                      type="server_host"                minOccurs="0"/>
          <xsd:element name="server_hosts"                     type="server_host_list"           minOccurs="0"/> <!-- Not Implemented -->
          <xsd:element name="ldap_sync_connector"              type="ldap_sync_connector"        minOccurs="0"/>
          <xsd:element name="ldap_sync_connectors"             type="ldap_sync_connector_list"   minOccurs="0"/>
          <xsd:element name="server_throttle"                  type="server_throttle"            minOccurs="0"/>
          <xsd:element name="server_throttles"                 type="server_throttle_list"       minOccurs="0"/>
          <xsd:element name="site_throttle"                    type="site_throttle"              minOccurs="0"/>
          <xsd:element name="site_throttles"                   type="site_throttle_list"         minOccurs="0"/>
          <xsd:element name="server_throttle_status"           type="server_throttle_status"     minOccurs="0"/>
          <xsd:element name="server_throttle_statuses"         type="server_throttle_status_list" minOccurs="0"/>
          <xsd:element name="site_throttle_status"             type="site_throttle_status"       minOccurs="0"/>
          <xsd:element name="site_throttles_statuses"          type="site_throttle_status_list"  minOccurs="0"/>

          <!-- base 64 encoded import file -->
          <xsd:element name="import_content"                   type="xsd:string"             minOccurs="0"/>
          <!-- import conflict details. If conflicts, one returned per object sent with import request -->
          <xsd:element name="import_conflict_details"          type="import_conflict_detail_list" minOccurs="0"/>
          <xsd:element name="hashed_string"       type="hashed_string"           minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="hashed_strings"      type="hashed_string_list"      minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="verify_signature"    type="verify_signature"        minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
        <xsd:attribute name="export_version" type="xsd:int"/>
      </xsd:complexType>
      <xsd:complexType name="import_conflict_detail">
        <xsd:all>
          <xsd:element name="type" type="xsd:string"/>
          <xsd:element name="name" type="xsd:string"/>
          <xsd:element name="diff" type="xsd:string"/>
          <xsd:element name="is_new" type="xsd:int"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="import_conflict_detail_list">
        <xsd:sequence>
          <xsd:element name="import_conflict_detail" type="import_conflict_detail" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="cache_filter">
        <xsd:all>
            <!--
              Specify which field the filter is matched against (by default filter is matched if it matches against any of the fields)
              Filter field can also be a path to a particular element in the response XML.
                For example:  queries/query/platform
            -->
            <xsd:element name="field"          type="xsd:string"  minOccurs="0"/>
            <xsd:element name="value"          type="xsd:string"  minOccurs="0"/>
            <!--
              The value_type specifies how the values are compared.
              String: standard lexicographical comparison (the default)
              Version: values are expected to be version strings, e.g. 9.4.2 is less than 10.1.3
              Numeric: numeric comparison, including decimal, floating point, and scientific notation
              IPAddress: values are expected to be IP addresses
              Date: a date in the format: YYYY-MM-DD HH:MM:SS
              DataSize: values are expected to be an expression of an amount of data, e.g. 125MB or 23K or 34.2Gig (numeric + B|K|M|G|T units)
              NumericInteger:  values are expected to be integer numeric values
            -->
            <xsd:element name="type" type="xsd:string" minOccurs="0"/>
            <!--
              The filter operator defines how the value(s) of the items being tested are compared against the value specified in the filter.
              Available operators are:
                RegexMatch: the item passes if its value matches the regular expression specified in the filter value
                Less, Greater, LessEqual, GreaterEqual, Equal: the item passes if its value is Less, Greater, LessEqual, GreaterEqual, Equal to the filter value
                The default is equal.
            -->
            <xsd:element name="operator"      type="xsd:string"  minOccurs="0"/>
            <xsd:element name="not_flag"      type="xsd:int"     minOccurs="0"/>   <!-- If set, the rows returned will be all the rows that do NOT match this filter definition -->
            <xsd:element name="and_flag"     type="xsd:int"        minOccurs="0"/> <!-- only used when sub_filters is specified -->
            <xsd:element name="sub_filters"   type="cache_filter_list"     minOccurs="0"/> <!-- Supported for ResultData only. If specified, all other properties except "not_flag" and "and_flag", will be ignored -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="cache_filter_list">
        <xsd:sequence>
          <xsd:element name="filter" type="cache_filter" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>
      <!-- one option per object in object_list -->
      <xsd:complexType name="import_conflict_options">
          <xsd:sequence>
              <!-- 0 = conflict error. 1 = overwrite. 2 = copy changing name, 3 = ignore. -->
              <xsd:element name="import_conflict_option" type="xsd:int" minOccurs="0" maxOccurs="unbounded"/>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="options">
        <xsd:all>
          <!--
            Bit array of flags, mostly for GetResultInfo/Data (note: flags not listed here must be specified by name):
              1: hide errors
              2: include answer times
              4: row counts only, for IDType "Action" selects between action status "summary" and "details"
              8: aggregate over time
              16: include most recent
              32: include hash values
              64: hide "no results"
              128: use user context (applies to GetSavedQuestions, and restricts results to only those visible by the user associated with the session )
          -->
          <xsd:element name="export_flag"           type="xsd:int"     minOccurs="0"/> <!-- used to tell server to export all data to a file in "Tanium Server\http\export" folder with name "<timestamp>.cvs". Related "<timestamp>.status" and "<timestamp>.qid" will be created in the same directory for progress tracking and debugging  -->
          <xsd:element name="export_format"         type="xsd:int"     minOccurs="0"/> <!-- 0 == csv format (backward compatible with console export), 1 == result xml format, similar to normal api use, 2 == CEF format, flattened, 3 == csv format, flattened if possible (single line in each cell) -->
          <xsd:element name="export_leading_text"   type="xsd:string"  minOccurs="0"/> <!-- when exporting, insert this text at the beginning of each line -->
          <xsd:element name="export_trailing_text"  type="xsd:string"  minOccurs="0"/> <!-- when exporting, append this text at the end of each line -->
          <xsd:element name="export_hide_csv_header_flag"  type="xsd:int"  minOccurs="0"/> <!-- when exporting in csv format, omit column header -->
          <xsd:element name="flags"                 type="xsd:int"     minOccurs="0"/>
          <xsd:element name="hide_errors_flag"      type="xsd:int"     minOccurs="0"/>
          <xsd:element name="include_answer_times_flag" type="xsd:int" minOccurs="0"/>
          <xsd:element name="row_counts_only_flag"  type="xsd:int"     minOccurs="0"/>
          <xsd:element name="aggregate_over_time_flag" type="xsd:int"  minOccurs="0"/>
          <xsd:element name="aggregate_by_value_flag" type="xsd:int"  minOccurs="0"/> <!-- For single-select question with force_computer_id_flag=1. If set, result data will be presented as one string hash per row with count. -->
          <xsd:element name="no_result_row_collation_flag" type="xsd:int"   minOccurs="0"/> <!-- If set, it will not stack up identical result rows.  Turn it on to get one row per computer with cid -->
          <xsd:element name="most_recent_flag"      type="xsd:int"     minOccurs="0"/>
          <xsd:element name="include_hashes_flag"   type="xsd:int"     minOccurs="0"/>
          <xsd:element name="hide_no_results_flag"  type="xsd:int"     minOccurs="0"/>
          <xsd:element name="use_user_context_flag" type="xsd:int"     minOccurs="0"/>
          <xsd:element name="script_data"           type="xsd:string"  minOccurs="0"/>   <!-- used to pass data between plugins -->
          <xsd:element name="return_lists_flag"     type="xsd:int"     minOccurs="0"/>   <!-- if set, result objects will be consolidated into a list tag, enabling the inclusion of "info" tag metadata -->
          <xsd:element name="return_cdata_flag"     type="xsd:int"     minOccurs="0"/>   <!-- if set, results will be returned in the ResultXML tag as raw xml wrapped in a CDATA tag instead of the result_object tag -->
          <xsd:element name="pct_done_limit"        type="xsd:int"     minOccurs="0"/>
          <xsd:element name="context_id"            type="xsd:int"     minOccurs="0"/>   <!-- Currently this is used by GetResultInfo/Data to specify the group_id of the issued questions, because saved_questions can be issued with different group ids in different contexts -->
          <!--
             samplefrequency: how far apart each sample should be (in seconds)
             sampleStart: how many samples into the past we should start with (0 == start with the most recent sample)
             sampleCount: how many samples we should examine

             Note: 600 seconds == 10 minutes, 10 minutes * 144 = one day
             Example: 600, 0, 144 means give me the last day at 10 minute resolution.
             Example: 600, 1440, 144 means give me the day starting from 11 days ago to 10 days ago at 10 minute resolution.

             Note: 3600 seconds == 1 hour, 1 hour * 168 = one week
             Example: 3600, 0, 168 means give me the last week at 1 hour resolution.
             Example: 3600, 168, 168 means give me the week before last week at 1 hour resolution.

             Note: if you ask for 168 samples, you may get fewer (if data is not available) but not more
          -->
          <xsd:element name="sample_frequency"      type="xsd:int"     minOccurs="0"/>
          <xsd:element name="sample_start"          type="xsd:int"     minOccurs="0"/>
          <xsd:element name="sample_count"          type="xsd:int"     minOccurs="0"/>
          <xsd:element name="audit_history_size"    type="xsd:int"     minOccurs="0"/> <!-- Used with object types like "audit_log" with type and object id specified, to limit number of entried returned. -->
          <xsd:element name="suppress_scripts"      type="xsd:int"     minOccurs="0"/>
          <xsd:element name="suppress_object_list"  type="xsd:int"     minOccurs="0"/> <!-- when performing add/update operations the original object_list will not be returned if this is set to 1.  defaults to 0 -->
          <!--
             you can select a subset of the result data, by specifying RowStart and RowCount, the order is controlled by SortOrder below
          -->
          <xsd:element name="row_start"             type="xsd:int"     minOccurs="0"/>
          <xsd:element name="row_count"             type="xsd:int"     minOccurs="0"/>
          <!--
             you can specify the sort order as a comma-separated list of column indices where the first column is column 1.
             a negative number indicates descending sort order.
             Example: "3,-2" means sort by the third column ascending first, and break ties by sorting by the second column descending
          -->
          <xsd:element name="sort_order"            type="xsd:string"  minOccurs="0"/>

          <!-- These filter what results are returned. For multiple filters if any one filter doesn't pass for an item the item is skipped. -->
          <xsd:element name="cache_filters" minOccurs="0" type="cache_filter_list"/>

          <!-- These two options are not used with cache_filters.  They have their own criteria -->
          <xsd:element name="filter_string"         type="xsd:string"  minOccurs="0"/>   <!-- Filter results to only include items that match this regular expression -->
          <xsd:element name="filter_not_flag"       type="xsd:int"     minOccurs="0"/>   <!-- If set, the rows returned will be all the rows that do NOT match the filter_string -->
          <!--
            recent_result_buckets is a comma separated list of integers.

            If empty or unspecified the default value is: "600,3600,86400,604800"

            When the most_recent_flag is set, results that are identical other than age will be grouped into age range buckets.
            By default, all ages less than 600 seconds will be in the first ("current results") group.
            The second group will contain all ages less than 3600 seconds but greater than or equal to 600.
            The final group will include all ages greater than the last specified range.
            You may include any number of buckets.
          -->
          <xsd:element name="recent_result_buckets" type="xsd:string"  minOccurs="0"/>

          <!--
               cache usage: requests that support a cache will respond with cache_info populated
               Using cache_id in subsequent requests will use this cache and have significant performance gains.
               cache_expiration is the number of seconds (600 max) the cache will remain in memory on the server.  Each request renews the specified cache.
               Setting cache_expiration to 0 will expire the cache.
          -->
          <xsd:element name="cache_id" type="xsd:long"        minOccurs="0"/>
          <xsd:element name="cache_expiration" type="xsd:int" minOccurs="0"/>
          <!--
              cache_sort_fields is used to sort the objects in a particular cache.
              only sorting of top level tags of SOAP objects is supported. (client_status/sensor/etc..)
              This is a comma delimited list with a - in front of the field name for reverse sort.
          -->
          <xsd:element name="cache_sort_fields"    type="xsd:string" minOccurs="0"/>
          <xsd:element name="include_user_details" type="xsd:int"    minOccurs="0"/>
          <xsd:element name="include_user_owned_object_ids_flag" type="xsd:int"    minOccurs="0"/> <!-- return owned object ID. Administrator only. -->
          <xsd:element name="include_hidden_flag"  type="xsd:int"    minOccurs="0"/>
          <xsd:element name="use_error_objects"    type="xsd:int"    minOccurs="0"/> <!-- on a failed soap request display the error details for a specific object instead of just an exception message -->
          <xsd:element name="use_json"             type="xsd:int"    minOccurs="0"/> <!-- return objects in JSON format if supported -->
          <xsd:element name="json_pretty_print"    type="xsd:int"    minOccurs="0"/> <!-- use readable format for exported JSON objects. -->
          <xsd:element name="live_snapshot_report_count_threshold"                type="xsd:int" minOccurs="0"/>
          <xsd:element name="live_snapshot_expiration_seconds"                    type="xsd:int" minOccurs="0"/>
          <xsd:element name="live_snapshot_always_use_seconds"                    type="xsd:int" minOccurs="0"/>
          <xsd:element name="live_snapshot_invalidate_report_count_percentage"    type="xsd:int" minOccurs="0"/>
          <xsd:element name="disable_live_snapshots"  type="xsd:int" minOccurs="0" maxOccurs="1"/>
          <xsd:element name="allow_cdata_base64_encode_flag"  type="xsd:int"    minOccurs="0"/> <!-- The serve will base64 encode the CDATA tag if this flag is on and there is invalid XML character in the result data. When data is encoded, an read-only option "cdata_base64_encoded" will be added as indicator. -->
          <xsd:element name="cdata_base64_encoded"  type="xsd:int"    minOccurs="0"/> <!-- Read only. See allow_base64_encode_flag for details. -->
          <xsd:element name="import_conflict_options" type="import_conflict_options" minOccurs="0"/> <!-- Import conflict ignore/overwrite options-->
          <xsd:element name="import_analyze_conflicts_only" type="xsd:int" minOccurs="0"/>    <!-- 1 if import should only preview conflicts -->
          <xsd:element name="export_dont_include_related" type="xsd:int" minOccurs="0"/> <!-- 1 if ExportObject should _not_ include related objects -->
          <xsd:element name="export_omit_soap_envelope" type="xsd:int" minOccurs="1"/>  <!-- 1 if ExportObject should only include the export, with no SOAP envelope -->
          <xsd:element name="import_existing_ignore_content_set" type="xsd:int" minOccurs="0"/> <!-- 1 if imported objects should stay in current content set if they already exist -->
          <xsd:element name="saved_question_qids_reissue_flag" type="xsd:int" minOccurs="0"/> <!-- 1 to reissue the specified saved question with group id in "context_id" -->
          <xsd:element name="saved_question_qids_allow_multiple_flag" type="xsd:int" minOccurs="0"/> <!-- Used to find all question ids (instead of the recent one) for a given saved question id -->
          <xsd:element name="saved_question_qids_include_expired_flag" type="xsd:int" minOccurs="0"/>
          <xsd:element name="saved_question_qids_ignore_mr_group_flag" type="xsd:int" minOccurs="0"/> <!-- admin only. Used to find all question ids for a given saved question id -->
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="content_set">
        <xsd:all>
          <xsd:element name="id" type="xsd:int" minOccurs="1" maxOccurs="1"></xsd:element>
          <xsd:element name="name" type="xsd:string" minOccurs="1" maxOccurs="1"></xsd:element>
          <xsd:element name="description" type="xsd:string" minOccurs="1" maxOccurs="1"></xsd:element>
          <!-- reserved name, typically for use by products as a reserved identifier -->
          <xsd:element name="reserved_name" type="xsd:string" minOccurs="1" maxOccurs="1"></xsd:element>
          <xsd:element name="metadata" type="metadata_list" minOccurs="0"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="content_set_list">
        <xsd:sequence>
          <xsd:element name="content_set" type="content_set" minOccurs="0" maxOccurs="unbounded"></xsd:element>
        </xsd:sequence>
      </xsd:complexType>"
      <xsd:complexType name="content_set_role_privilege_on_role">
        <xsd:all>
            <xsd:element name="id" type="xsd:int" minOccurs="1" maxOccurs="1"></xsd:element>
            <xsd:element name="content_set" type="id_reference" minOccurs="0" maxOccurs="1"></xsd:element>
            <xsd:element name="content_set_privilege" type="id_reference" minOccurs="1" maxOccurs="1"></xsd:element>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="content_set_role_privilege_on_role_list">
          <xsd:sequence>
              <xsd:element name="content_set_role_privilege" type="content_set_role_privilege_on_role" minOccurs="0" maxOccurs="unbounded"></xsd:element>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="content_set_role">
        <xsd:all>
          <xsd:element name="id" type="xsd:int" minOccurs="1" maxOccurs="1"></xsd:element>
          <xsd:element name="name" type="xsd:string" minOccurs="1" maxOccurs="1"></xsd:element>
          <xsd:element name="description" type="xsd:string" minOccurs="1" maxOccurs="1"></xsd:element>
          <!-- reserved name, typically for use by products as a reserved identifier -->
          <xsd:element name="reserved_name" type="xsd:string" minOccurs="1" maxOccurs="1"></xsd:element>
          <xsd:element name="metadata" type="metadata_list" minOccurs="0"/>
          <xsd:element name="deny_flag" type="xsd:int" minOccurs="1" maxOccurs="1"></xsd:element>
          <xsd:element name="all_content_sets_flag" type="xsd:int" minOccurs="1" maxOccurs="1"></xsd:element>
          <!-- for add/update only, can be used to replace the content_set_role_privilege objects for this role -->
          <!-- note that the content_set_role of each content_role_privilege is ignored... containing role specifies that -->
          <xsd:element name="content_set_role_privileges" type="content_set_role_privilege_on_role_list" minOccurs="0" omitByDefault="1"/>
          <!-- this allows us to determine what category the role is (reserved, micro-admin, module, advanced (content set) -->
          <xsd:element name="category" type="xsd:string" minOccurs="1" maxOccurs="1"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="content_set_role_list">
        <xsd:sequence>
          <xsd:element name="content_set_role" type="content_set_role" minOccurs="0" maxOccurs="unbounded"></xsd:element>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="content_set_role_membership">
          <xsd:all>
              <xsd:element name="id" type="xsd:int" minOccurs="1" maxOccurs="1"></xsd:element>
              <xsd:element name="user" type="user" minOccurs="1" maxOccurs="1"></xsd:element>
              <xsd:element name="content_set_role" type="id_reference" minOccurs="1" maxOccurs="1"></xsd:element>
          </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="content_set_role_membership_list">
        <xsd:sequence>
          <xsd:element name="content_set_role_membership" type="content_set_role_membership" minOccurs="0" maxOccurs="unbounded"></xsd:element>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="content_set_user_group_role_membership">
          <xsd:all>
              <xsd:element name="id" type="xsd:int" minOccurs="1" maxOccurs="1"></xsd:element>
              <xsd:element name="user_group" type="id_reference" minOccurs="1" maxOccurs="1"></xsd:element>
              <xsd:element name="content_set_role" type="id_reference" minOccurs="1" maxOccurs="1"></xsd:element>
          </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="content_set_user_group_role_membership_list">
        <xsd:sequence>
           <xsd:element name="content_set_user_group_role_membership" type="content_set_user_group_role_membership" minOccurs="0" maxOccurs="unbounded"></xsd:element>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="content_set_privilege">
        <xsd:all>
            <xsd:element name="id" type="xsd:int" minOccurs="1" maxOccurs="1"></xsd:element>
            <xsd:element name="name" type="xsd:string" minOccurs="1" maxOccurs="1"></xsd:element>
            <!-- reserved name, typically for use by products as a reserved identifier -->
            <xsd:element name="reserved_name" type="xsd:string" minOccurs="1" maxOccurs="1"></xsd:element>
            <xsd:element name="privilege_type" type="xsd:string" minOccurs="1" maxOccurs="1"></xsd:element>
            <xsd:element name="privilege_module" type="xsd:string" minOccurs="1" maxOccurs="1"></xsd:element>
            <xsd:element name="metadata" type="metadata_list" minOccurs="0"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="content_set_privilege_list">
          <xsd:sequence>
              <xsd:element name="content_set_privilege" type="content_set_privilege" minOccurs="0" maxOccurs="unbounded"></xsd:element>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="content_set_role_privilege">
          <xsd:all>
              <xsd:element name="id" type="xsd:int" minOccurs="1" maxOccurs="1"></xsd:element>
              <xsd:element name="content_set" type="id_reference" minOccurs="0" maxOccurs="1"></xsd:element>
              <xsd:element name="content_set_role" type="id_reference" minOccurs="1" maxOccurs="1"></xsd:element>
              <xsd:element name="content_set_privilege" type="id_reference" minOccurs="1" maxOccurs="1"></xsd:element>
          </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="content_set_role_privilege_list">
          <xsd:sequence>
              <xsd:element name="content_set_role_privilege" type="content_set_role_privilege" minOccurs="0" maxOccurs="unbounded"></xsd:element>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="content_set_privilege_list">
      <xsd:sequence>
          <xsd:element name="content_set_privilege" type="content_set_privilege"  minOccurs="0" maxOccurs="unbounded"></xsd:element>
      </xsd:sequence>
      </xsd:complexType>
      <!-- only supports GetObject. Returns effective content set privileges. -->
      <xsd:complexType name="effective_content_set_privilege">
        <xsd:all>
          <xsd:element name="content_set" type="content_set" minOccurs="1" maxOccurs="1"></xsd:element>
          <xsd:element name="content_set_privilege_list" type="content_set_privilege_list" minOccurs="1" maxOccurs="1"></xsd:element>
        </xsd:all>
      </xsd:complexType>
      <!-- Can optionally specify a user ID to retrieve effective privileges for another user (if admin or content set admin only) -->
      <xsd:complexType name="effective_content_set_privilege_request">
        <xsd:all>
          <xsd:element name="user" type="user" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="effective_content_set_privilege_list">
        <xsd:sequence>
           <xsd:element name="effective_content_set_privilege" type="effective_content_set_privilege"  minOccurs="0" maxOccurs="unbounded"></xsd:element>
        </xsd:sequence>
      </xsd:complexType>
        <xsd:complexType name="dashboard">
            <xsd:all>
                <xsd:element name="id" type="xsd:int"></xsd:element>
                <xsd:element name="name" type="xsd:string"></xsd:element>
                <xsd:element name="user" type="user"></xsd:element>
                <xsd:element name="public_flag" type="xsd:int"></xsd:element>
                <xsd:element name="content_set" type="content_set"></xsd:element>
                <xsd:element name="group" type="group"></xsd:element>
                <xsd:element name="text" type="xsd:string"></xsd:element>
                <!-- if present on update, replaces the list of questions based on id, in order -->
                <xsd:element name="saved_question_list" type="saved_question_list"></xsd:element>
            </xsd:all>
        </xsd:complexType>
        <xsd:complexType name="dashboard_list">
            <xsd:sequence>
                <xsd:element name="dashboard" type="dashboard" minOccurs="0" maxOccurs="unbounded"></xsd:element>
            </xsd:sequence>
        </xsd:complexType>
      <xsd:complexType name="dashboard_group">
          <xsd:all>
              <xsd:element name="id" type="xsd:int" minOccurs="1"></xsd:element>
              <xsd:element name="name" type="xsd:string"></xsd:element>
              <xsd:element name="user" type="user"></xsd:element>
              <xsd:element name="public_flag" type="xsd:int"></xsd:element>
              <xsd:element name="editable_flag" type="xsd:int"></xsd:element>
              <xsd:element name="other_flag" type="xsd:int"></xsd:element>
              <xsd:element name="text" type="xsd:string"></xsd:element>
              <xsd:element name="content_set" type="content_set"></xsd:element>
              <xsd:element name="display_index" type="xsd:int"></xsd:element>
              <!-- base64 encoded icon image -->
              <xsd:element name="icon" type="xsd:string"></xsd:element>
              <!-- if present on update, replaces the list of dashboards based on id, in order -->
              <xsd:element name="dashboard_list" type="dashboard_list"></xsd:element>
          </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="user_group">
          <xsd:all>
              <xsd:element name="id" type="xsd:int" minOccurs="1"></xsd:element>
              <xsd:element name="name" type="xsd:string"></xsd:element>
              <xsd:element name="user_list" type="user_list" omitByDefault="1"></xsd:element>
              <!-- for add/update only, can be used to replace the content_set_user_group_role_membership objects for this user_group -->
              <xsd:element name="content_set_roles" type="content_set_role_list" minOccurs="0" omitByDefault="1"/>
              <!-- management rights group -->
              <xsd:element name="group" type="group" minOccurs="0"></xsd:element>
              <xsd:element name="deleted_flag"   type="xsd:int" minOccurs="0"></xsd:element>
              <xsd:element name="exclusive_flag" type="xsd:int" minOccurs="0"></xsd:element>
          </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="user_group_list">
          <xsd:sequence>
              <xsd:element name="user_group" type="user_group" minOccurs="0" maxOccurs="unbounded"></xsd:element>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="solution">
          <xsd:all>
              <xsd:element name="id" type="xsd:int"></xsd:element>
              <xsd:element name="solution_id" type="xsd:string" minOccurs="1"></xsd:element>
              <xsd:element name="name" type="xsd:string"></xsd:element>
              <xsd:element name="imported_version" type="xsd:string"></xsd:element>
              <xsd:element name="signature" type="xsd:string"></xsd:element>
              <xsd:element name="last_update" type="xsd:string"></xsd:element>
              <xsd:element name="dup_resolve_type" type="xsd:int"></xsd:element>
              <xsd:element name="imported_by" type="xsd:string"></xsd:element>
              <xsd:element name="description" type="xsd:string"></xsd:element>
              <xsd:element name="category" type="xsd:string"></xsd:element>
              <xsd:element name="installed_xml_url" type="xsd:string"></xsd:element>
              <xsd:element name="delete_xml_url" type="xsd:string"></xsd:element>
              <xsd:element name="deleted_flag" type="xsd:int"></xsd:element>
          </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="solution_list">
          <xsd:sequence>
              <xsd:element name="solution" type="solution" minOccurs="0" maxOccurs="unbounded"></xsd:element>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="action_group">
          <xsd:all>
              <xsd:element name="id" type="xsd:int" minOccurs="1"></xsd:element>
              <xsd:element name="name" type="xsd:string"></xsd:element>
              <xsd:element name="groups"   type="group_list" minOccurs="0"/>
              <xsd:element name="and_flag" type="xsd:int"></xsd:element>
              <!-- if public_flag is off, only administrator can see this action group -->
              <xsd:element name="public_flag" type="xsd:int"></xsd:element>
              <!-- user_groups is only valid if public_flag is on. An empty list means all user can see this action group -->
              <xsd:element name="user_groups" type="user_group_list" minOccurs="0"/>
              <xsd:element name="deleted_flag" type="xsd:int"></xsd:element>
          </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="action_group_list">
          <xsd:sequence>
              <xsd:element name="action_group" type="action_group" minOccurs="0" maxOccurs="unbounded"></xsd:element>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="saved_question_package_specs">
          <xsd:all>
              <xsd:element name="saved_question" type="id_reference" minOccurs="1" maxOccurs="1"></xsd:element>
              <xsd:element name="packages"       type="package_spec_list" minOccurs="0" maxOccurs="1"></xsd:element>
          </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="saved_question_question">
          <xsd:all>
              <!-- Use these options to reissue or filter: context_id, saved_question_qids_reissue_flag, saved_question_qids_allow_multiple_flag, saved_question_qids_include_expired_flag, saved_question_qids_ignore_mr_group_flag-->
              <xsd:element name="saved_question" type="id_reference" minOccurs="1" maxOccurs="1"></xsd:element>
              <xsd:element name="questions"       type="question_list" minOccurs="0" maxOccurs="1"></xsd:element>
          </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="saved_question_question_list">
          <xsd:sequence>
              <xsd:element name="saved_question_question" type="saved_question_question" minOccurs="0" maxOccurs="unbounded"></xsd:element>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="ldap_sync_connector_list">
          <xsd:sequence>
              <xsd:element name="ldap_sync_connector" type="ldap_sync_connector" minOccurs="0" maxOccurs="unbounded"></xsd:element>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="ldap_sync_connector">
          <xsd:all>
             <xsd:element name="id"   type="xsd:int"   minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="name" type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="enable" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="host"   type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="port" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="secure" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="use_ntlm" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="ldap_user"   type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="ldap_password"   type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="base_users"   type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="filter_users"   type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="members_only_flag"   type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="user_id"   type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="user_name"   type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="user_domain"   type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="user_display_name"   type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="user_member_of"   type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="base_groups"   type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="filter_groups"   type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="group_id"   type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="group_name"   type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="group_member"   type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="last_sync_timestamp" type="xsd:string"  minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="last_sync_result" type="xsd:string"  minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="disable_ldap_auth" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="disable_referrals_flag" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
          </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="server_throttle_list">
          <xsd:sequence>
             <xsd:element name="server_throttle" type="server_throttle" minOccurs="0" maxOccurs="unbounded"></xsd:element>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="server_throttle">
         <xsd:all>
             <xsd:element name="id"   type="xsd:int"   minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="name" type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="ip_address" type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="bandwidth_bytes_limit" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="connection_limit" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="download_bandwidth_bytes_limit" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="download_connection_limit" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="sensor_bandwidth_bytes_limit" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="sensor_connection_limit" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="deleted_flag" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
         </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="site_throttle_list">
          <xsd:sequence>
             <xsd:element name="site_throttle" type="site_throttle" minOccurs="0" maxOccurs="unbounded"></xsd:element>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="site_throttle">
         <xsd:all>
             <xsd:element name="id"   type="xsd:int"   minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="name" type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="subnets" type="site_throttle_subnet_list" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="bandwidth_bytes_limit" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="download_bandwidth_bytes_limit" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="sensor_bandwidth_bytes_limit" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="all_subnets_flag" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="deleted_flag" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
         </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="site_throttle_subnet_list">
          <xsd:sequence>
              <xsd:element name="subnet" type="site_throttle_subnet" minOccurs="0" maxOccurs="unbounded"></xsd:element>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="site_throttle_subnet">
          <xsd:all>
              <xsd:element name="range" type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
          </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="server_throttle_status_list">
          <xsd:sequence>
             <xsd:element name="server_throttle_status" type="server_throttle_status" minOccurs="0" maxOccurs="unbounded"></xsd:element>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="server_throttle_status">
         <xsd:all>
             <xsd:element name="id"   type="xsd:int"   minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="name" type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="queue_delay_milliseconds" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="download_queue_delay_milliseconds" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="sensor_queue_delay_milliseconds" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
         </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="site_throttle_status_list">
          <xsd:sequence>
             <xsd:element name="site_throttle_status" type="site_throttle_status" minOccurs="0" maxOccurs="unbounded"></xsd:element>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="site_throttle_status">
         <xsd:all>
             <xsd:element name="id"   type="xsd:int"   minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="name" type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="subnets" type="site_throttle_subnet_status_list" minOccurs="0" maxOccurs="1"></xsd:element>
         </xsd:all>
      </xsd:complexType>
      <xsd:complexType name="site_throttle_subnet_status_list">
          <xsd:sequence>
              <xsd:element name="subnet" type="site_throttle_subnet_status" minOccurs="0" maxOccurs="unbounded"></xsd:element>
          </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="site_throttle_subnet_status">
          <xsd:all>
              <xsd:element name="range" type="xsd:string" minOccurs="0" maxOccurs="1"></xsd:element>
              <xsd:element name="queue_delay_milliseconds" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="download_queue_delay_milliseconds" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
             <xsd:element name="sensor_queue_delay_milliseconds" type="xsd:int" minOccurs="0" maxOccurs="1"></xsd:element>
          </xsd:all>
      </xsd:complexType>
        <xsd:complexType name="computer_id_list">
            <xsd:sequence>
                <xsd:element name="id"                 type="xsd:int"         minOccurs="0" maxOccurs="unbounded"/>
            </xsd:sequence>
        </xsd:complexType>
        <xsd:complexType name="hashed_string">
            <xsd:all>
                <xsd:element name="sensor_hash"        type="xsd:int"          minOccurs="1" maxOccurs="1"/>         <!-- The hash that identifies which sensor generated this string -->
                <xsd:element name="value_hash"         type="xsd:int"          minOccurs="1" maxOccurs="1"/>         <!-- The hash that identifies which string value was generated by the sensor -->
                <xsd:element name="which_computer_id"  type="xsd:int"          minOccurs="0" maxOccurs="1"/>         <!-- If specified, and a collision has occurred, this value will be used to select the first or second of the two collision values, IF POSSIBLE -->
                <!-- Based on the input values specified above, the values below will be returned: -->
                <xsd:element name="value"              type="xsd:string"       minOccurs="0" maxOccurs="1"/>         <!-- The actual string value that was generated by the sensor, or an error string, like [result currently unavailable] or [hash collision detected] -->
                <xsd:element name="error_flag"         type="xsd:int"          minOccurs="0" maxOccurs="1"/>         <!-- If this is non-zero then that indicates that this string value is considered to be an error message and will be filtered out if errors are hidden -->
                <xsd:element name="collision_flag"     type="xsd:int"          minOccurs="0" maxOccurs="1"/>         <!-- If this is non-zero then that indicates that a hash collision occurred, and there are two string values that result in the same hash -->
                <xsd:element name="first_collision"    type="xsd:string"       minOccurs="0" maxOccurs="1"/>         <!-- If collision_flag is set, then this will be the value of the first of the two strings that result in the same hash -->
                <xsd:element name="second_collision"   type="xsd:string"       minOccurs="0" maxOccurs="1"/>         <!-- If collision_flag is set, then this will be the value of the second of the two strings that result in the same hash -->
                <xsd:element name="first_computer_id"  type="computer_id_list" minOccurs="0" maxOccurs="unbounded"/> <!-- If collision_flag is set, then this MAY indicate the computer ids of clients that generated the first of the two collision values -->
                <xsd:element name="second_computer_id" type="computer_id_list" minOccurs="0" maxOccurs="unbounded"/> <!-- If collision_flag is set, then this MAY indicate the computer ids of clients that generated the second of the two collision values -->
            </xsd:all>
        </xsd:complexType>
        <xsd:complexType name="hashed_string_list">
            <xsd:sequence>
                <xsd:element name="hashed_string"      type="hashed_string"   minOccurs="0" maxOccurs="unbounded"/>
            </xsd:sequence>
        </xsd:complexType>
        <xsd:element name="tanium_soap_request" type="typens:TaniumSOAPRequest" />
      <xsd:element name="return" type="typens:TaniumSOAPResult" />
    </xsd:schema>
  </types>
  <!-- Message for Tanium SOAP API -->
  <message name="Request">
    <part name="tanium_soap_request" element="typens:tanium_soap_request"/>
  </message>
  <message name="Response">
    <part name="return" element="typens:return"/>
  </message>
  <!-- Port for Tanium SOAP API -->
  <portType name="TaniumSOAPPort">
    <operation name="Request">
      <input message="typens:Request"/>
      <output message="typens:Response"/>
    </operation>
  </portType>
  <!-- Binding for Tanium SOAP API - Document, SOAP over HTTP -->
  <binding name="TaniumSOAPBinding" type="typens:TaniumSOAPPort">
    <soap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
    <operation name="Request">
      <soap:operation soapAction="urn:TaniumSOAPAction"/>
      <input>
        <soap:body use="literal" namespace="urn:TaniumSOAP"/>
      </input>
      <output>
        <soap:body use="literal" namespace="urn:TaniumSOAP"/>
      </output>
    </operation>
  </binding>
  <!-- Endpoint for Tanium SOAP API -->
  <service name="TaniumSOAPService">
    <port name="TaniumSOAPPort" binding="typens:TaniumSOAPBinding">
      <soap:address location="http://soap.tanium.com/soap"/>
    </port>
  </service>
</definitions>


"""  # noqa
