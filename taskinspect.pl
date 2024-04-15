#!/usr/bin/perl

use strict;
use warnings;
use REST::Client;
use GitLab::API::v4;
use JSON::XS;
use Data::Dumper qw(Dumper);
use String::Util 'trim';

# The user that we want to check for.
my $user = "lruzicka";
my $startdate = "2024-04-07";
# Read the tokens from the file
open(FH, '<', 'gitlab_token') or die $!;
    my $gitlab_token = <FH>;
    $gitlab_token = trim $gitlab_token;
close(FH);

open(FH, '<', 'gnome_token') or die $!;
    my $gnome_token = <FH>;
    $gnome_token = trim $gnome_token;
close(FH);


sub read_from_api {
    my ($host, $params) = @_;
    my $restapi = REST::Client->new();
    $restapi->setHost($host);
    my $stream = $restapi->GET($params);
    my $response = $stream->responseContent();
    return $response;
}

sub check_Bugzilla {
    my $host = 'https://bugzilla.redhat.com';
    my $params = "/rest/bug?chfieldfrom=$startdate &chfieldto=Now&email1=$user&emailreporter1=1&emailtype1=substring";
    my $json = read_from_api($host, $params);
    my $data = decode_json($json);
    # Print the results
    print("===== Bugs reported within RedHat Bugzilla. =====\n");
    my $bugs = $data->{bugs};
    foreach my $bug (@$bugs) {
        print("$bug->{summary} ($host/$bug->{id})\n");
    };
    print("\n");
}

#sub check_AskFedora {
#    my $url = "https://discussion.fedoraproject.org";
#    my $params = "/u/$user/activity";
#    my $json = read_from_api($url, $params);
#    print(Dumper($json));
#}

sub check_GnomeLab {
    my $api = GitLab::API::v4->new(
        url => "https://gitlab.gnome.org/api/v4",
        private_token => $gnome_token
    );
    my %params = ('username' => $user, 'created_after' => $startdate);
    my $json = $api->global_issues(\%params);
    print(" ===== Issues reported withing gitlab.gnome.org. =====\n");
    foreach my $issue (@$json) {
        print("$issue->{title}: $issue->{references}->{full}\n");
    }
    print("\n");

}

sub check_GitLab {
    my $api = GitLab::API::v4->new(
        url => "https://gitlab.com/api/v4",
        private_token => $gitlab_token
    );
    my %params = ('owned' => 'Yes');
    my $json = $api->projects(\%params);
    print("===== Commits pushed to gitlab.org ===== \n");
    foreach my $project (@$json) {
        print("----- $project->{name}: $project->{id} ----- \n");
        %params = ('author' => $user, 'since' => $startdate);
        my $commits = $api->commits($project->{id}, \%params);
        foreach my $commit (@$commits) {
            print("     - $commit->{title}\n");
        }

    }
    print("\n");

}
check_Bugzilla();
check_GnomeLab();
check_GitLab();

